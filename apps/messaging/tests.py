from django.test import TestCase

import uuid
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from apps.organizations.models import Application, Offer, Organization
from apps.candidates.models import CandidateProfile
from apps.core.models import Country, Cause
from .models import Conversation, Message, ConversationParticipant

User = get_user_model()


class MessagingModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="pass")
        self.country = Country.objects.create(name="France", code="FR")
        self.cause = Cause.objects.create(name="Education")
        self.org = Organization.objects.create(name="Test Org", country=self.country)
        self.candidate_profile = CandidateProfile.objects.create(user=self.user)
        self.offer = Offer.objects.create(
            organization=self.org,
            title="Test Offer",
            description="Desc",
            country=self.country,
            cause=self.cause,
        )
        self.application = Application.objects.create(
            offer=self.offer,
            candidate=self.candidate_profile,
            status="pending",
        )

    def test_conversation_str_with_application(self):
        conv = Conversation.objects.create(application=self.application)
        self.assertIn("Conversation for application", str(conv))

    def test_unread_count(self):
        conv = Conversation.objects.create(subject="Test")
        ConversationParticipant.objects.create(conversation=conv, user=self.user)
        other_user = User.objects.create_user(email="other@example.com", password="pass")
        ConversationParticipant.objects.create(conversation=conv, user=other_user)
        
        Message.objects.create(conversation=conv, sender=other_user, content="Hello")
        self.assertEqual(conv.unread_count_for(self.user), 1)
        
        Message.objects.create(conversation=conv, sender=self.user, content="Reply")
        self.assertEqual(conv.unread_count_for(self.user), 1)  # own message doesn't count


class MessagingAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="user@example.com", password="pass")
        self.other_user = User.objects.create_user(email="other@example.com", password="pass")
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        
        self.conv = Conversation.objects.create(subject="Project X")
        ConversationParticipant.objects.create(conversation=self.conv, user=self.user)
        ConversationParticipant.objects.create(conversation=self.conv, user=self.other_user)

    def test_list_conversations(self):
        response = self.client.get("/api/messaging/conversations/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)

    def test_create_message(self):
        data = {"conversation": str(self.conv.id), "content": "Hello world"}
        response = self.client.post("/api/messaging/messages/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["sender_email"], "user@example.com")

    def test_mark_read(self):
        Message.objects.create(conversation=self.conv, sender=self.other_user, content="Unread")
        response = self.client.post(f"/api/messaging/conversations/{self.conv.id}/mark_read/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Message.objects.filter(is_read=False).count(), 0)

    def test_non_participant_cannot_message(self):
        outsider = User.objects.create_user(email="outsider@example.com", password="pass")
        self.client.force_authenticate(user=outsider)
        data = {"conversation": str(self.conv.id), "content": "Hack"}
        response = self.client.post("/api/messaging/messages/", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

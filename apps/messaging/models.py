# apps/messaging/models.py
import uuid

from django.conf import settings
from django.db import models
from django.db.models import Count, Q


class Conversation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    application = models.OneToOneField(
        "engagement.Application",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="conversation",
    )
    subject = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        db_table = "conversations"

    def __str__(self):
        if self.application:
            return f"Conversation for application #{str(self.application.id)[:8]}"
        return f"Conversation: {self.subject or 'No subject'}"

    @property
    def last_message(self):
        return self.messages.order_by("-sent_at").first()

    def unread_count_for(self, user):
        if not user or not user.is_authenticated:
            return 0
        return self.messages.filter(is_read=False).exclude(sender=user).count()

    def mark_all_read_for(self, user):
        """Mark all messages as read for a specific user."""
        self.messages.filter(is_read=False).exclude(sender=user).update(is_read=True)


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="messages",
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="sent_messages",
    )
    content = models.TextField()
    attachment_url = models.URLField(blank=True)
    is_read = models.BooleanField(default=False)
    sent_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["sent_at"]
        db_table = "messages"

    def __str__(self):
        sender_email = self.sender.email if self.sender else "Deleted user"
        return f"Message from {sender_email} at {self.sent_at}"


class ConversationParticipant(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name="participants",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="conversations",
    )
    joined_at = models.DateTimeField(auto_now_add=True)
    is_archived = models.BooleanField(default=False)

    class Meta:
        unique_together = ["conversation", "user"]
        db_table = "conversation_participants"

    def __str__(self):
        return f"{self.user.email} in conversation {str(self.conversation.id)[:8]}"
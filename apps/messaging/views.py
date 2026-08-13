# apps/messaging/views.py
from django.db.models import Count, Prefetch, Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated ,AllowAny
from rest_framework.response import Response
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Conversation, ConversationParticipant, Message
from .permissions import IsConversationParticipant, IsMessageSenderOrReadOnly
from .serializers import (
    ConversationCreateSerializer,
    ConversationDetailSerializer,
    ConversationListSerializer,
    MessageCreateSerializer,
    MessageSerializer,
)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = "page_size"
    max_page_size = 100


# =============================================================================
# CONVERSATION VIEWS
# =============================================================================

class ConversationListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ConversationCreateSerializer
        return ConversationListSerializer

    def get_queryset(self):
        user = self.request.user
        queryset = (
            Conversation.objects.filter(participants__user=user)
            .annotate(participant_count=Count("participants"))
            .prefetch_related(
                Prefetch(
                    "messages",
                    queryset=Message.objects.order_by("-sent_at"),
                    to_attr="last_message_list",
                )
            )
        )

        # Filter by application
        application_id = self.request.query_params.get("application")
        if application_id:
            queryset = queryset.filter(application_id=application_id)

        # Filter archived/unarchived
        archived = self.request.query_params.get("archived")
        if archived is not None:
            is_archived = archived.lower() == "true"
            queryset = queryset.filter(
                participants__user=user, participants__is_archived=is_archived
            )

        return queryset.distinct()

    def perform_create(self, serializer):
        serializer.save()


class ConversationDetailView(generics.RetrieveAPIView):
    serializer_class = ConversationDetailSerializer
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    lookup_field = "pk"

    def get_queryset(self):
        return Conversation.objects.prefetch_related(
            "messages__sender",
            "participants__user",
        ).annotate(participant_count=Count("participants"))


class ConversationMarkReadView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    lookup_field = "pk"

    def get_queryset(self):
        return Conversation.objects.all()

    def post(self, request, *args, **kwargs):
        conversation = self.get_object()
        conversation.mark_all_read_for(request.user)
        return Response(
            {"detail": "All messages marked as read."},
            status=status.HTTP_200_OK,
        )


class ConversationArchiveView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    lookup_field = "pk"

    def get_queryset(self):
        return Conversation.objects.all()

    def post(self, request, *args, **kwargs):
        conversation = self.get_object()
        participant = get_object_or_404(
            ConversationParticipant,
            conversation=conversation,
            user=request.user,
        )
        participant.is_archived = not participant.is_archived
        participant.save()
        return Response(
            {
                "detail": f"Conversation {'archived' if participant.is_archived else 'unarchived'}."
            },
            status=status.HTTP_200_OK,
        )


# =============================================================================
# MESSAGE VIEWS
# =============================================================================

class MessageListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated, IsConversationParticipant]
    pagination_class = StandardResultsSetPagination
    

    def perform_create(self, serializer):
        message = serializer.save(sender=self.request.user)
        
        # Broadcast to all participants
        channel_layer = get_channel_layer()
        for participant in message.conversation.participants.all():
            if participant != self.request.user:
                async_to_sync(channel_layer.group_send)(
                    f"user_{participant.id}",
                    {
                        "type": "chat_message",
                        "message": {
                            "id": str(message.id),
                            "content": message.content,
                            "conversation_id": str(message.conversation.id),
                            "sender": {"id": str(message.sender.id), "name": message.sender.get_full_name()},
                            "created_at": message.created_at.isoformat(),
                        },
                    }
                )
    def get_serializer_class(self):
        if self.request.method == "POST":
            return MessageCreateSerializer
        return MessageSerializer

    def get_conversation(self):
        conversation_id = self.kwargs.get("conversation_pk")
        conversation = get_object_or_404(Conversation, pk=conversation_id)

        # Verify participation
        if not ConversationParticipant.objects.filter(
            conversation=conversation, user=self.request.user
        ).exists():
            raise PermissionDenied("You are not a participant in this conversation.")

        return conversation

    def get_queryset(self):
        conversation = self.get_conversation()
        return Message.objects.filter(conversation=conversation).select_related(
            "sender"
        )

    def perform_create(self, serializer):
        conversation = self.get_conversation()
        serializer.save(
            conversation=conversation,
            sender=self.request.user,
        )


class MessageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsMessageSenderOrReadOnly]
    lookup_field = "pk"

    def get_queryset(self):
        conversation_id = self.kwargs.get("conversation_pk")
        return Message.objects.filter(conversation_id=conversation_id).select_related(
            "sender"
        )

    def perform_update(self, serializer):
        # Only allow editing content, and only for a short window (e.g., 15 min)
        instance = self.get_object()
        from django.utils import timezone
        from datetime import timedelta

        if timezone.now() - instance.sent_at > timedelta(minutes=15):
            raise ValidationError("Messages can only be edited within 15 minutes.")

        serializer.save()


# =============================================================================
# UNREAD COUNT (Global)
# =============================================================================

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def unread_messages_count(request):
    """Return total unread messages across all conversations for the user."""
    count = Message.objects.filter(
        conversation__participants__user=request.user,
        is_read=False,
    ).exclude(sender=request.user).count()

    return Response({"unread_count": count})
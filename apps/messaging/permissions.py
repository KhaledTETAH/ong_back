# apps/messaging/permissions.py
from rest_framework import permissions

from .models import ConversationParticipant


class IsConversationParticipant(permissions.BasePermission):
    """
    Only allow access if the user is a participant in the conversation.
    """

    def has_object_permission(self, request, view, obj):
        # obj is a Conversation
        return ConversationParticipant.objects.filter(
            conversation=obj, user=request.user
        ).exists()


class IsMessageSenderOrReadOnly(permissions.BasePermission):
    """
    Allow reading messages if participant, but only edit/delete own messages.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions for any participant
        if request.method in permissions.SAFE_METHODS:
            return ConversationParticipant.objects.filter(
                conversation=obj.conversation, user=request.user
            ).exists()

        # Write permissions only for sender
        return obj.sender == request.user
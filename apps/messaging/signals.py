# apps/messaging/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.engagement.models import Application  

from .models import Conversation, ConversationParticipant


@receiver(post_save, sender=Application)
def create_conversation_on_application(sender, instance, created, **kwargs):
    """
    Auto-create a conversation when an Application is submitted.
    Adjust field names based on your actual Application model.
    """
    if created:
        conversation = Conversation.objects.create(
            application=instance,
            subject=f"Application: {instance.job_posting.title}",
        )

        # Add candidate and recruiter as participants
        # Adjust these based on your actual model relationships
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=instance.candidate.user,
        )
        ConversationParticipant.objects.create(
            conversation=conversation,
            user=instance.job_posting.recruiter,
        )
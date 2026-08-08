# apps/messaging/serializers.py
from rest_framework import serializers

from apps.accounts.serializers import UserMinimalSerializer
from apps.core.models import Skill 

from .models import Conversation, ConversationParticipant, Message


class MessageSerializer(serializers.ModelSerializer):
    sender = UserMinimalSerializer(read_only=True)
    sender_id = serializers.UUIDField(write_only=True, required=False)

    class Meta:
        model = Message
        fields = [
            "id",
            "conversation",
            "sender",
            "sender_id",
            "content",
            "attachment_url",
            "is_read",
            "sent_at",
        ]
        read_only_fields = ["id", "sent_at", "is_read"]


class MessageCreateSerializer(serializers.ModelSerializer):
    """Used when creating a message. Conversation is inferred from URL."""
    class Meta:
        model = Message
        fields = ["content", "attachment_url"]


class ConversationParticipantSerializer(serializers.ModelSerializer):
    user = UserMinimalSerializer(read_only=True)

    class Meta:
        model = ConversationParticipant
        fields = ["user", "joined_at", "is_archived"]


class ConversationListSerializer(serializers.ModelSerializer):
    last_message = MessageSerializer(read_only=True)
    unread_count = serializers.SerializerMethodField()
    participant_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Conversation
        fields = [
            "id",
            "subject",
            "application",
            "last_message",
            "unread_count",
            "participant_count",
            "created_at",
            "updated_at",
        ]

    def get_unread_count(self, obj: Conversation) -> int:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.unread_count_for(request.user)
        return 0


class ConversationDetailSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)
    participants = ConversationParticipantSerializer(
        "participants", many=True, read_only=True
    )
    unread_count = serializers.SerializerMethodField()

    class Meta:
        model = Conversation
        fields = [
            "id",
            "subject",
            "application",
            "messages",
            "participants",
            "unread_count",
            "created_at",
            "updated_at",
        ]

    def get_unread_count(self, obj: Conversation) -> int:
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            return obj.unread_count_for(request.user)
        return 0


class ConversationCreateSerializer(serializers.ModelSerializer):
    """For creating a new conversation with initial participants."""
    participant_ids = serializers.ListField(
        child=serializers.UUIDField(),
        write_only=True,
        min_length=1,
    )
    initial_message = serializers.CharField(
        write_only=True, required=False, allow_blank=True
    )

    class Meta:
        model = Conversation
        fields = ["subject", "application", "participant_ids", "initial_message"]

    def validate_participant_ids(self, value):
        request_user = self.context["request"].user
        if request_user.id not in value:
            value.append(request_user.id)
        # Remove duplicates while preserving order
        seen = set()
        return [x for x in value if not (x in seen or seen.add(x))]

    def create(self, validated_data):
        participant_ids = validated_data.pop("participant_ids")
        initial_message = validated_data.pop("initial_message", "")
        application = validated_data.get("application")

        # If application-linked, auto-set participants from application
        if application:
            # Adjust based on your Application model fields
            participant_ids = [
                application.candidate.user_id,
                application.job_posting.recruiter_id,
            ]

        conversation = Conversation.objects.create(**validated_data)

        # Create participants
        for user_id in participant_ids:
            ConversationParticipant.objects.create(
                conversation=conversation,
                user_id=user_id,
            )

        # Create initial message if provided
        if initial_message:
            Message.objects.create(
                conversation=conversation,
                sender=self.context["request"].user,
                content=initial_message,
            )

        return conversation
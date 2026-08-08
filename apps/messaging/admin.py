from django.contrib import admin
# apps/messaging/admin.py
from django.contrib import admin

from .models import Conversation, ConversationParticipant, Message


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ["sent_at"]
    ordering = ["-sent_at"]


class ParticipantInline(admin.TabularInline):
    model = ConversationParticipant
    extra = 0
    readonly_fields = ["joined_at"]


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "application", "created_at", "updated_at"]
    list_filter = ["created_at"]
    search_fields = ["subject", "application__id"]
    inlines = [ParticipantInline, MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ["id", "conversation", "sender", "is_read", "sent_at"]
    list_filter = ["is_read", "sent_at"]
    search_fields = ["content", "sender__email"]
    readonly_fields = ["sent_at"]


@admin.register(ConversationParticipant)
class ConversationParticipantAdmin(admin.ModelAdmin):
    list_display = ["conversation", "user", "joined_at", "is_archived"]
    list_filter = ["is_archived", "joined_at"]
    search_fields = ["user__email", "conversation__id"]

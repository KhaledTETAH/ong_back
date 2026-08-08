# apps/messaging/urls.py
from django.urls import path

from . import views

app_name = "messaging"

urlpatterns = [
    # Conversations
    path(
        "conversations/",
        views.ConversationListCreateView.as_view(),
        name="conversation-list",
    ),
    path(
        "conversations/<pk>/",
        views.ConversationDetailView.as_view(),
        name="conversation-detail",
    ),
    path(
        "conversations/<uuid:pk>/mark-read/",
        views.ConversationMarkReadView.as_view(),
        name="conversation-mark-read",
    ),
    path(
        "conversations/<uuid:pk>/archive/",
        views.ConversationArchiveView.as_view(),
        name="conversation-archive",
    ),
    # Messages within a conversation
    path(
        "conversations/<uuid:conversation_pk>/messages/",
        views.MessageListCreateView.as_view(),
        name="message-list",
    ),
    path(
        "conversations/<uuid:conversation_pk>/messages/<uuid:pk>/",
        views.MessageDetailView.as_view(),
        name="message-detail",
    ),
    # Global unread count
    path(
        "unread-count/",
        views.unread_messages_count,
        name="unread-count",
    ),
]
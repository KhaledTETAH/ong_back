import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]
        if self.user.is_anonymous:
            await self.close()
            return

        # Each user listens to their own personal group
        self.room_group_name = f"user_{self.user.id}"

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Handle messages sent FROM React via WS (optional — see hybrid note below)"""
        data = json.loads(text_data)
        message_type = data.get("type")

        if message_type == "typing":
            # Broadcast typing to conversation participants
            await self.channel_layer.group_send(
                f"conversation_{data['conversation_id']}",
                {
                    "type": "typing_indicator",
                    "user_id": str(self.user.id),
                    "conversation_id": data["conversation_id"],
                },
            )

    async def chat_message(self, event):
        """Receive broadcast FROM channel layer and send to React"""
        await self.send(text_data=json.dumps({
            "type": "new_message",
            "message": event["message"],
        }))

    async def typing_indicator(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "user_id": event["user_id"],
            "conversation_id": event["conversation_id"],
        }))

    async def unread_update(self, event):
        await self.send(text_data=json.dumps({
            "type": "unread_update",
            "conversation_id": event.get("conversation_id"),
            "count": event.get("count"),
        }))
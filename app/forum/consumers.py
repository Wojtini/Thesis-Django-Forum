import json

from channels.generic.websocket import AsyncWebsocketConsumer


class ThreadConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        room_group_name = self.scope["url_route"]["kwargs"]["thread_id"]
        await self.channel_layer.group_add(
            room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data, **kwargs):
        pass

    async def update_thread(self, event):
        await self.send(
            text_data=json.dumps(
                {
                    "origin": event.get("origin_user"),
                    "content": event.get("content"),
                }
            )
        )

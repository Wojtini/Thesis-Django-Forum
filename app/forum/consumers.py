import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class ThreadConsumer(WebsocketConsumer):
    def connect(self):
        room_group_name = self.scope["url_route"]["kwargs"]["thread_id"]
        async_to_sync(self.channel_layer.group_add)(
            room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        pass

    def update_thread(self, event):
        self.send(text_data=event.get("content"))

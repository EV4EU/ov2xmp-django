# consumers.py
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class UsersConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        # Join the users_updates channel group
        await self.channel_layer.group_add('users_updates', self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave the group
        await self.channel_layer.group_discard('users_updates', self.channel_name)

    async def websocket_send(self, event):
        # Send a message to the WebSocket client
        await self.send_json({
            "message": event["text"]
        })

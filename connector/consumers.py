from channels.generic.websocket import AsyncJsonWebsocketConsumer


class ConnectorConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        """
        Called when a WebSocket connection is established
        """
        # Join the connector updates group
        await self.channel_layer.group_add(
            "connector_updates",
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """
        Called when a WebSocket connection is closed
        """
        await self.channel_layer.group_discard(
            "connector_updates",
            self.channel_name
        )

    async def connector_update(self, event):
        """
        Handler for connector update events
        """
        # Send the update to the WebSocket
        await self.send_json(content=event['data'])

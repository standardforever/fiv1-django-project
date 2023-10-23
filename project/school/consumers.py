from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # You can use a fixed group name for the Raspberry Pi
        self.raspberry_pi_group_name = "raspberry_pi"

        # Join the Raspberry Pi group
        await self.channel_layer.group_add(
            self.raspberry_pi_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave the Raspberry Pi group
        await self.channel_layer.group_discard(
            self.raspberry_pi_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # Send the message to the Raspberry Pi group
        await self.channel_layer.group_send(
            self.raspberry_pi_group_name,
            {
                "type": "raspberry_pi.message",
                "message": message,
            }
        )

    async def raspberry_pi_message(self, event):
        message = event["message"]
        # print(message)
        # Send the message to the WebSocket (Raspberry Pi)
        await self.send(text_data=json.dumps({"message": message}))

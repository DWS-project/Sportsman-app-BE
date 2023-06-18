from channels.generic.websocket import WebsocketConsumer
import json
from asgiref.sync import async_to_sync


class SocketConsumer(WebsocketConsumer):
    def connect(self):
        # Add the socket connection to the 'mysocket' group
        self.room_group_name = 'room'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Remove the socket connection from the 'mysocket' group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def send_message(self, event):
        # Send the socket message to the connected clients
        message = event['message']
        self.send(text_data=json.dumps(message))

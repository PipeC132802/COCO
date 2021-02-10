import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.db.models import Q
from notify.models import Notification

from Apps.ManageChats.models import Message


class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['username']
        self.room_group_name = 'notification_%s' % self.room_name
        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        if text_data_json["type"] == "new_notification":
            text_data_json["unread_notifications"] = self.get_unread_notifications(text_data_json)
        elif text_data_json["type"] == "new_msg":
            text_data_json['unread_msgs'] = self.get_unread_msgs(text_data_json)
        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            text_data_json
        )

    # Receive message from room group
    def new_notification(self, event):
        self.send(text_data=json.dumps(event))

    def new_msg(self, event):
        self.send(text_data=json.dumps(event))

    @staticmethod
    def get_unread_notifications(event):
        return Notification.objects.filter(recipient__username=event['receiver'], read=False).count()

    @staticmethod
    def get_unread_msgs(event):
        return Message.objects.filter(
            (Q(conversation__owner__username=event["receiver"]) |
             Q(conversation__opponent__username=event["receiver"])),
            read=False
        ).exclude(sender__username=event["receiver"]).count()

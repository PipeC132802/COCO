from rest_framework import serializers

from Apps.ManageChats.models import Message


class MessageSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.username')

    class Meta:
        model = Message
        fields = ['conversation', 'sender_username', 'text', 'read', 'created', 'is_removed']


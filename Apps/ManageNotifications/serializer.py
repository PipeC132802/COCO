from notify.models import Notification
from rest_framework import serializers

from Apps.ManageNotifications.models import NotificationsPreference


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id']


class NotificationPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotificationsPreference
        fields = ['push', 'email', 'sms', 'user']

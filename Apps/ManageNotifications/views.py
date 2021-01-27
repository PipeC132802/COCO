import asyncio

from asgiref.sync import sync_to_async
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import classonlymethod
from notify.models import Notification
from rest_framework import generics

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Apps.ManageNotifications.serializer import NotificationSerializer
from COCO.functions import get_profile_url


class NotificationsListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Notification
    #serializer_class = NotificationSerializer

    def get(self, request, *args, **kwargs):

        notifications = Notification.objects.filter(recipient_id=request.user.pk)[:50]
        notifications_list = []
        for notification in notifications:

            if not notification.read:
                notification.mark_as_read()
            if notification.nf_type == 'reacted_by_one_user' and notification.obj.reaction:
                notification_dictionary = self.get_reaction_notification_json(notification)
            elif notification.nf_type == 'barter_commented':
                notification_dictionary = self.get_comment_notification_json(notification)
            elif notification.nf_type == 'accepted_by_user':
                notification_dictionary = self.get_accept_notification_json(notification)
            elif notification.nf_type == 'followed_by_user' and notification.obj.status == 1:

                notification_dictionary = self.get_follow_notification_json(notification)
            else:
                notification_dictionary = {}
            notifications_list.append(notification_dictionary)

        return Response(notifications_list, status=200)

    @staticmethod
    def get_reaction_notification_json(notification):
        return {
            'receiver': notification.recipient.username,
            'reaction': notification.obj.reaction,
            'userFrom': {
                'username': notification.actor.username,
                'name': '{0} {1}'.format(notification.actor.first_name, notification.actor.last_name),
                'profile_picture': get_profile_url(notification.actor)
            },
            'action': notification.verb,
            'barter': notification.target.serializer(),
            'field': 'reaction',
            'created': notification.created
        }

    @staticmethod
    def get_comment_notification_json(notification):
        return {
            'receiver': notification.recipient.username,
            'comment': {
                'text': notification.obj.comment,
                'id': notification.obj.pk
            },
            'userFrom': {
                'username': notification.actor.username,
                'name': '{0} {1}'.format(notification.actor.first_name, notification.actor.last_name),
                'profile_picture': get_profile_url(notification.actor)
            },
            'action': notification.verb,
            'barter': notification.target.serializer(),
            'field': 'comment',
            'created': notification.created
        }

    @staticmethod
    def get_accept_notification_json(notification):
        return {
            'receiver': notification.recipient.username,
            'comment': {
                'text': notification.target.comment,
                'id': notification.target.pk
            },
            'userFrom': {
                'username': notification.actor.username,
                'name': '{0} {1}'.format(notification.actor.first_name, notification.actor.last_name),
                'profile_picture': get_profile_url(notification.actor)
            },
            'action': notification.verb,
            'barter': notification.obj.serializer(),
            'field': 'comment',
            'created': notification.created
        }

    @staticmethod
    def get_follow_notification_json(notification):
        return {
            'receiver': notification.recipient.username,
            'userFrom': {
                'username': notification.actor.username,
                'name': '{0} {1}'.format(notification.actor.first_name, notification.actor.last_name),
                'profile_picture': get_profile_url(notification.actor)
            },
            'action': notification.verb,
            'field': 'follow',
            'created': notification.created
        }



from django.http import JsonResponse
from django.shortcuts import render
from notify.models import Notification
from rest_framework import generics

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from COCO.functions import get_profile_url


class NotificationsListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    model = Notification

    def get(self, request, *args, **kwargs):
        notifications = Notification.objects.filter(recipient_id=request.user.pk)
        notifications_list = []
        for notification in notifications:
            if notification.nf_type == 'reacted_by_one_user' and notification.obj.reaction:
                notification_dictionary = self.get_reaction_notification_json(notification)
                notifications_list.append(notification_dictionary)
            notification.mark_as_read()

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
        }

    def get_obj_context(self, notification):

        target = self.get_target(notification)
        return {
            'type': notification.nf_type,
            'actor': {
                'username': notification.actor.username,
                'name': '{0} {1}'.format(notification.actor.first_name, notification.actor.last_name),
                'profile_picture': get_profile_url(user=notification.actor)
            },
            'verb': notification.verb,
            'description': notification.description,
            'target': target,
            'created': notification.created,
            'read': notification.read
        }

    def get_target(self, notification):
        # TO-DO get notification target
        if notification.nf_type == 'reacted_by_one_user':
            target = notification.target
        elif notification.nf_type == 'commented_by_one_user':
            target = ''
        elif notification.nf_type == 'reviewed_by_one_user':
            target = ''
        elif notification.nf_type == 'followed_by_one_user':
            target = ''
        return target

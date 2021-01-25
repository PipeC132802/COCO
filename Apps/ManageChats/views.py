from django.db.models import Q
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Apps.ManageChats.models import Message
from Apps.ManageChats.serializer import MessageSerializer
from COCO.functions import get_profile_url


class ChatsListApi(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        messages = Message.objects.filter(
            Q(conversation__owner_id=request.user.pk) |
            Q(conversation__opponent_id=request.user.pk)).distinct("conversation").order_by('conversation', '-created')
        messages_list = []
        messages = list(reversed(sorted(messages, key=lambda message: message.created)))
        for message in messages:
            msg_dictionary = message.serializer()
            opponent = self.get_opponent(request.user, message)
            msg_dictionary["opponent"] = {
                'username': opponent.username,
                'name': '{0} {1}'.format(opponent.first_name, opponent.last_name),
                'profile_picture': get_profile_url(opponent),
            }
            msg_dictionary["id"] = message.pk
            msg_dictionary["unread_messages"] = Message.objects.filter(conversation=message.conversation,
                                                                       read=False).exclude(sender=request.user).count()

            messages_list.append(msg_dictionary)
        return Response(messages_list, status=200)

    @staticmethod
    def get_opponent(user, msg):
        if user.username == msg.conversation.owner.username:
            opponent = msg.conversation.opponent
        else:
            opponent = msg.conversation.owner
        return opponent


class MessagesApi(generics.ListAPIView):
    model = Message
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(conversation_id=self.request.GET["conversation"]).order_by("created")

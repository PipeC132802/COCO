from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import DestroyAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from Apps.ManageUsers.models import UserProfilePhoto


class UserStatus(generics.RetrieveAPIView):  # , LoginRequiredMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        user = request.user

        try:
            profile_picture = UserProfilePhoto.objects.get(
                user_id=user.pk).profile_picture.url
        except:
            profile_picture = ''
        """unread_messages = Message.objects.filter(
            (Q(conversation__owner_id=request.user.pk) |
             Q(conversation__opponent_id=request.user.pk)),
            read=False
        ).count()
        unread_notifications = 3"""
        unread_notifications = 5
        unread_messages = 3
        return JsonResponse({
            'username': user.username,
            'name': user.first_name + ' ' + user.last_name,
            'profile_picture': profile_picture,
            'unread_notifications': unread_notifications,
            'unread_messages': unread_messages,
        })


class LogoutApi(DestroyAPIView):
    """
    Delete the Token object
    assigned to the current User object.
    Accepts/Returns nothing.
    """
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        response = self.logout(request)
        return JsonResponse(response)

    def logout(self, request):
        response = {}
        try:
            token = request.META['HTTP_AUTHORIZATION'].split(' ')[1]
            #Token.objects.filter(key=token, user=request.user).delete()
            response['logout'] =True
        except:
            response['logout'] = False
        return response



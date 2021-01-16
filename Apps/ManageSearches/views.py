from time import time

from django.db.models import Q
# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from Apps.ManageBarters.models import BarterAbout
from Apps.ManageUsers.models import UserAbout


def serialize_barters(model):
    barter_list = []
    for barter_about in model:
        barter_json = {
            'id': barter_about.barter.pk,
        }
        barter_list.append(barter_json)
    return barter_list


def get_barters(request):
    query = request.GET['q']
    barters = BarterAbout.objects.filter(
        Q(barter__barter_title__icontains=query) | Q(barter__user__username__icontains=query) |
        Q(description__icontains=query) | Q(barter__user__first_name__icontains=query) | Q(
            barter__user__last_name__icontains=query), barter__deleted=False).distinct('barter_id')

    return serialize_barters(barters)


def get_users(request):
    query = request.GET['q']
    users_abouts = UserAbout.objects.filter(Q(bio__icontains=query) | Q(user__username__icontains=query) |
                                            Q(user__first_name__icontains=query) | Q(
        user__last_name__icontains=query)).distinct('user_id')
    users_json = [user_about.serializer() for user_about in users_abouts]
    return users_json


class SearchApi(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        start_time = time()
        try:
            field = request.GET['field']
        except:
            field = None

        response = {'order': ['barters', 'users']}
        if field is None:
            response['barters'] = get_barters(request)
            response['users'] = get_users(request)

        elif field == 'barters':
            response['barters'] = get_barters(request)
            response['users'] = {}
        elif field == 'users':
            response['barters'] = {}
            response['users'] = get_users(request)
        response['time'] = str(time() - start_time)[:5]
        return Response(response, status=200)

from django.shortcuts import render

# Create your views here.
from rest_framework import generics


class SearchApi(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        try:
            field = request.GET['field']
        except:
            field = None
        #TO-DO
        response = {}
        if field is None:
            response['barters'] = self.get_barters(request)
            response['users'] = self.get_users(request)

        elif field == 'barters':
            response['barters'] = self.get_barters(request)
        elif field == 'users':
            response['users'] = self.get_users(request)
            response = self.get_users()

    def get_barters(self, request):
        barters_json = {}


    def get_users(self, request):
        users_json = { }
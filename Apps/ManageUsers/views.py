from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse, HttpResponse
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.views import APIView

from Apps.ManageUsers.models import UserProfilePhoto, VerifyUser
from COCO.mailing import sendMail


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


class CreateUserApi(generics.CreateAPIView):
    def post(self, request, *args, **kwargs):
        first_name = request.data['first_name']
        last_name = request.data['last_name']
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()

            token = Token.objects.create(user=user)
            return JsonResponse({
                'created': True,
                'key': token.key
            })

        except:
            return Response({'status': 'Ya existe una cuenta asociada a este correo o nombre de usuario'}, status=409)


class ResetUserPasswordApi(APIView):
    def get(self, request, *args, **kwargs):
        token = request.GET['token']
        print(token)
        return Response({'Get': True})

    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        aim = request.data["aim"]
        try:
            user = User.objects.get(email=email)
            token_generator = PasswordResetTokenGenerator()
            token = token_generator.make_token(user)
            try:
                token_in_db = VerifyUser.objects.get(user=user)
                if token_in_db.token != token:
                    token_in_db.token = token
                    token_in_db.save()
            except:
                token_in_db = VerifyUser.objects.create(user=user, token=token)
            self.send_mail(token_in_db, aim.upper())
            return Response({'verificationToken': True}, status=200)
        except:
            return Response({'verificationToken': False}, status=403)

    def send_mail(self, instance, aim):
        name = '{0} {1}'.format(instance.user.first_name, instance.user.last_name)
        subject = 'Confirmación de tu correo electrónico'
        description = []
        if aim == 'CHANGE':
            description.append(
                'Solicitaste cambiar tu contraseña y para ello es necesario que confirmes tu correo electrónico'
            )
        else:
            description.append(
                'Vamos a confirmar tu correo electrónico para que puedas usar COCO, construyendo comunidad alrededor del conocimiento.'
            )
        description.append('Para continuar pulsa el botón que está a continuación:')
        token = instance.token
        link = 'http://localhost:8080/verify-email'
        context = {
            'name': name,
            'subject': subject,
            'description': description,
            'token': token,
            'link': link
        }
        configs = {
            'Template': 'Mail/mail-template.html',
            'subject': subject,
            'to': [instance.user.email],
        }

        sendMail(configs, context)

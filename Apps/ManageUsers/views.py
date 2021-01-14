from datetime import datetime

from PIL import Image
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.http import JsonResponse
from notify.models import Notification
from rest_framework import generics
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from Apps.ManageUsers.models import UserProfilePhoto, VerifyUser, Area, Place, UserContact, UserAbout, UserSkill, \
    UserInterest, UserRelationship
from Apps.ManageUsers.serializer import AreaSerializer, UserAboutSerializer, UserSerializer
from COCO.functions import save_areas, get_place
from COCO.mailing import sendMail
from COCO.settings import DOMAIN, BASE_DIR, PIXABAY_API_KEY


class UserStatus(generics.RetrieveAPIView):  # , LoginRequiredMixin):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        user = request.user
        try:
            profile_picture = DOMAIN + UserProfilePhoto.objects.get(
                user_id=user.pk).profile_picture.url
        except:
            profile_picture = ''
        """unread_messages = Message.objects.filter(
            (Q(conversation__owner_id=request.user.pk) |
             Q(conversation__opponent_id=request.user.pk)),
            read=False
        ).count()
        unread_notifications = 3"""
        unread_notifications = Notification.objects.filter(recipient_id=request.user.pk, read=False).count()
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


class UserVerificationApi(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        token = request.GET['token']
        try:
            VerifyUser.objects.get(user=request.user, token=token)
            return Response({'user_verified': True}, status=200)
        except:
            return Response({'user_verified': False}, status=400)

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
                'Solicitaste cambiar tu contraseña y para ello es necesario que confirmes tu correo electrónico.'
            )
        else:
            description.append(
                'Vamos a confirmar tu correo electrónico para que puedas usar COCO, construyendo comunidad alrededor del conocimiento.'
            )
        description.append('Para continuar pulsa el botón que está a continuación:')
        token = instance.token
        link = 'http://localhost:8080/'
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


class AreaListApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AreaSerializer
    model = Area

    def get_queryset(self):
        return Area.objects.filter(area__icontains=self.request.GET["area"])


class UserContactApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        country = request.data["country"]
        city = request.data["city"]
        phone_number = request.data["phone_number"]
        place = get_place(country, city)
        try:
            UserContact.objects.create(user=request.user, cellphone=phone_number, place=place)
            return JsonResponse({'contact_created': True})
        except:
            user_contact = UserContact.objects.get(user=request.user)
            user_contact.cellphone = phone_number
            user_contact.place = place
            user_contact.save()
            return JsonResponse({'contact_updated': True})


class UserAboutAndAreasApi(generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        gender = request.data["gender"]
        birthday = request.data["birthday"]
        bio = request.data["bio"]
        skills = request.data["skills"]
        learn = request.data["learn"]

        save_areas(skills, request.user, UserSkill)
        save_areas(learn, request.user, UserInterest)

        try:
            UserAbout.objects.create(user=request.user, bio=bio, birthday=birthday, gender=gender)

            return JsonResponse({'contact_created': True, 'key': PIXABAY_API_KEY})
        except:
            """user_about = UserAbout.objects.get(user=request.user)
            user_about.bio = bio
            user_about.birthday = birthday
            user_about.gender = gender"""
            return JsonResponse({'Error': "There's invalid data."})


class ProfilePictureApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        profile_picture = request.FILES.get("profile_picture")
        try:
            profile_picture_obj = UserProfilePhoto.objects.create(user=request.user, profile_picture=profile_picture)
            self.resize_img(profile_picture_obj)
            return JsonResponse({'profile_picture_created': True})
        except:
            return Response({'profile_picture_created': False}, status=500)

    def resize_img(self, profile_picture):
        import cv2 as cv
        path = str(BASE_DIR) + '/Files/' + str(profile_picture.profile_picture)
        img = cv.imread(path)
        height, width = img.shape[:2]

        # if ratio eidth/heigth is greater than 0.1, crop image (square format)
        if abs(height / width - 1) > 0.1:
            if height < width:
                image = img[0: height, int(width / 2) - int(height / 2): int(width / 2) + int(height / 2)]

            else:
                image = img[int(height / 2) - int(width / 2): int(height / 2) + int(width / 2), 0: width]

            # save current profile_picture in its path
            # encode_param = [int(cv.IMWRITE_JPEG_QUALITY), 90]
            # result, encimg = cv.imencode('.jpg', image, encode_param)
            cv.imwrite(path, image)
            im = Image.open(path)
            im.save(path, format="JPEG", quality=50)


class UserAccountInfoApi(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        username = request.GET["username"]
        username_request = request.GET["username_request"]

        try:
            user_profile = UserProfilePhoto.objects.get(user__username=username)
            user_json = {
                'name': "{0} {1}".format(user_profile.user.first_name, user_profile.user.last_name),
                'profile_picture': DOMAIN + user_profile.profile_picture.url,
                'date_joined': user_profile.user.date_joined,
                'followers': UserRelationship.objects.filter(user_to__username=username, status=1).count(),
                'following': UserRelationship.objects.filter(user_from__username=username, status=1).count(),
                'skills': [user_skill.area.area for user_skill in UserSkill.objects.filter(user__username=username)],
                'follow_this_user': UserRelationship.objects.filter(user_from__username=username_request,
                                                                    user_to__username=username,
                                                                    status=1).exists(),
                'follow_you': UserRelationship.objects.filter(user_from__username=username,
                                                              user_to__username=username_request,
                                                              status=1).exists()
            }
        except:
            try:
                user = User.objects.get(username=username)
                user_json = {
                    'name': "{0} {1}".format(user.first_name, user.last_name),
                    'profile_picture': '',
                    'skills': [user_skill.area.area for user_skill in
                               UserSkill.objects.filter(user__username=username)],
                    'date_joined': user.date_joined.strftime("Se unión en %B de %Y"),
                    'followers': UserRelationship.objects.filter(user_to__username=username, status=1).count(),
                    'following': UserRelationship.objects.filter(user_from__username=username, status=1).count(),
                    'follow_this_user': UserRelationship.objects.filter(user_from__username=username_request,
                                                                        user_to__username=username,
                                                                        status=1).exists(),
                    'follow_you': UserRelationship.objects.filter(user_from__username=username,
                                                                  user_to__username=username_request,
                                                                  status=1).exists()
                }
            except User.DoesNotExist:
                return Response("User not found", status=404)

        return JsonResponse(user_json)


class UserAboutApi(generics.RetrieveAPIView):
    serializer_class = UserAboutSerializer
    model = UserAbout

    def get(self, request, *args, **kwargs):
        try:
            user_about = UserAbout.objects.get(user__username=self.request.GET["username"])
            return Response(user_about.serializer(), status=200)
        except:
            # Loggin error
            return Response('User info not found', status=404)


class UserContactAndAreasApi(generics.RetrieveAPIView):
    serializer_class = UserAboutSerializer

    def get(self, request, *args, **kwargs):
        try:
            username = self.request.GET["username"]
            user_contact = UserContact.objects.get(user__username=username)
            user_json = user_contact.serializer()
            user_json["interests"] = ", ".join(
                [user_interest.area.area for user_interest in UserInterest.objects.filter(user__username=username)])
            user_json["skills"] = ", ".join(
                [user_skill.area.area for user_skill in UserSkill.objects.filter(user__username=username)])
            return Response(user_json, status=200)
        except:
            # Loggin error
            return Response('User info not found', status=404)


class FollowUserApi(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        username_from = request.GET["username_from"]
        username_to = request.GET["username_to"]
        try:
            follow_status = UserRelationship.objects.get(user_from__username=username_from,
                                                         user_to__username=username_to, status=1)
            follow_status = follow_status.status
        except:
            follow_status = 0
        return Response({
            'follow_this_user': follow_status
        })

    def post(self, request, *args, **kwargs):
        username_from = request.data["username_from"]
        username_to = request.data["username_to"]
        target = request.data["target"]
        try:
            follow_status = UserRelationship.objects.get(user_from__username=username_from,
                                                         user_to__username=username_to)
            if follow_status.status != 2:
                if follow_status.status == 1:
                    follow_status.status = 0
                else:
                    follow_status.status = 1

                follow_status.save()
        except:
            user_from = User.objects.get(username=username_from)
            user_to = User.objects.get(username=username_to)
            follow_status = UserRelationship.objects.create(user_from=user_from, user_to=user_to, status=1)
        if target == 'self':
            following = UserRelationship.objects.filter(user_from__username=username_from, status=1).count()
            followers = UserRelationship.objects.filter(user_to__username=username_from, status=1).count()
        else:
            following = UserRelationship.objects.filter(user_from__username=username_to, status=1).count()
            followers = UserRelationship.objects.filter(user_to__username=username_to, status=1).count()

        return Response({
            'following': following,
            'followers': followers,
            'follow_this_user': follow_status.status
        })


class SuggestUserApi(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        id_users_following = [user_relationship.user_to.pk for user_relationship in
                              UserRelationship.objects.filter(user_from=user, status=1)]
        try:
            id_users_following.append(User.objects.get(username=request.GET["user_except"]).pk)
        except:
            pass
        user_interests = [user_interest.area.area for user_interest in
                          UserInterest.objects.filter(user__username=user.username).distinct('user')]
        users = [user_skill.user for user_skill in UserSkill.objects.filter(area__area__in=user_interests).exclude(
            user__in=id_users_following).distinct()[:5]]
        json_response = []
        for user in users:
            try:
                profile_picture = DOMAIN + UserProfilePhoto.objects.get(user=user).profile_picture.url
            except:
                profile_picture = ''
            dic = {
                'name': '{0} {1}'.format(user.first_name, user.last_name),
                'username': user.username,
                'profile_picture': profile_picture,
            }
            json_response.append(dic)

        return Response(json_response, status=200)


class FollowApi(generics.ListAPIView):

    def get(self, request, *args, **kwargs):
        username_target = request.GET["username_target"]
        username_request = request.GET["username_request"]
        field = request.GET["field"]
        if field == 'followers':
            follow_list = UserRelationship.objects.filter(user_to__username=username_target, status=1)
        elif field == 'following':
            follow_list = UserRelationship.objects.filter(user_from__username=username_target, status=1)
        response = self.get_context(follow_list, field, username_request)
        return Response(response)

    def get_context(self, follow_list, field, username_request):
        json_obj = []
        for follow_item in follow_list:
            if field == 'followers':
                try:
                    profile_picture = DOMAIN + UserProfilePhoto.objects.get(
                        user=follow_item.user_from).profile_picture.url
                except:
                    profile_picture = ''
                dic = {
                    'name': '{0} {1}'.format(follow_item.user_from.first_name, follow_item.user_from.last_name),
                    'username': follow_item.user_from.username,
                    'profile_picture': profile_picture,
                    'follow': UserRelationship.objects.filter(user_from__username=username_request,
                                                              user_to=follow_item.user_from).exists()
                }

            elif field == 'following':
                try:
                    profile_picture = DOMAIN + UserProfilePhoto.objects.get(
                        user=follow_item.user_to).profile_picture.url
                except:
                    profile_picture = ''
                dic = {
                    'name': '{0} {1}'.format(follow_item.user_to.first_name, follow_item.user_to.last_name),
                    'username': follow_item.user_to.username,
                    'profile_picture': profile_picture,
                    'follow': UserRelationship.objects.filter(user_from__username=username_request,
                                                              user_to=follow_item.user_to).exists()
                }
            json_obj.append(dic)
        return json_obj


class UpdateUserAccountInfoApi(generics.RetrieveAPIView, generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, *args, **kwargs):

        skills = request.data["skills"]
        learn = request.data["interests"]

        self.save_personal_info(request)
        self.save_user_about(request)
        self.save_user_contact(request)

        save_areas(skills, request.user, UserSkill)
        save_areas(learn, request.user, UserInterest)
        return Response({'Detail': 'User info edited successfully'}, status=200)

    def save_personal_info(self, request):
        first_name = request.data["first_name"]
        last_name = request.data["last_name"]
        user = request.user
        user.first_name = first_name
        user.last_name = last_name
        user.save()

    def save_user_about(self, request):
        bio = request.data["bio"]
        try:
            user_about = UserAbout.objects.get(user=request.user)
        except:
            user_about = UserAbout.objects.create(user=request.user)
        user_about.bio = bio
        user_about.save()

    def save_user_contact(self, request):
        country = request.data["country"]
        city = request.data["city"]
        place = Place.objects.filter(country__icontains=country, city__icontains=city)
        if place.exists():
            place = place[0]
        else:
            place = Place.objects.create(country=country, city=city)
        cellphone = request.data["cellphone"]
        try:
            user_contact = UserContact.objects.get(user=request.user)
        except:
            user_contact = UserContact.objects.create(user=request.user, place=place)
        user_contact.cellphone = cellphone
        user_contact.place = place
        user_contact.save()

    def get(self, request, *args, **kwargs):
        user = request.user
        user_contact = UserContact.objects.get(user=user)
        user_about = UserAbout.objects.get(user=user)
        user_skills = UserSkill.objects.filter(user=user)
        user_interests = UserInterest.objects.filter(user=user)
        try:
            cellphone = user_contact.cellphone.split(' ')[1]
            prefix = user_contact.cellphone.split(' ')[0]
        except:
            cellphone, prefix = '', ''
        response = {
            'first_name': user.first_name,
            'last_name': user.last_name,
            'country': user_contact.place.country,
            'city': user_contact.place.city,
            'cellphone': cellphone,
            'prefix': prefix,
            'bio': user_about.bio,
            'skills': [user_skill.area.area for user_skill in user_skills],
            'interests': [user_interest.area.area for user_interest in user_interests]
        }
        return Response(response, status=200)

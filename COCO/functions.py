import base64
from datetime import datetime

from notify.models import Notification
from rest_framework.response import Response

from Apps.ManageUsers.models import Area, Place, UserProfilePhoto
from COCO.mailing import send_mail_with_file
from COCO.settings import DOMAIN


def save_areas(areas, user, obj_param):
    obj_param.objects.filter(user=user).delete()
    for area in areas:
        if len(area):
            try:
                area_in_db = Area.objects.get(area__icontains=area)
            except:
                area_in_db = Area.objects.create(area=area.capitalize())
            try:
                obj_param.objects.get(user=user, area=area_in_db)
            except:
                obj_param.objects.create(user=user, area=area_in_db)


def get_place(country, city):
    try:
        place = Place.objects.get(country__icontains=country, city__icontains=city)
    except:
        place = Place.objects.create(country=country.capitalize(), city=city.capitalize())
    return place


from rest_framework import generics


def get_profile_url(user):
    try:
        profile_picture = DOMAIN + UserProfilePhoto.objects.get(user=user).profile_picture.url
    except:
        profile_picture = ''
    return profile_picture


def get_img_url_from_model(model, query):
    try:
        field = DOMAIN + model.objects.get(query).photo.url
    except:
        field = ''
    return field


def get_notification_and_mark_as_unread(query):
    notifications = Notification.objects.filter(query)
    for notification in notifications:
        notification.created = datetime.now()
        notification.mark_as_unread()


class SendBug(generics.RetrieveAPIView):
    def post(self, request, *args, **kwargs):
        img = request.FILES.get("img")
        if img is not None:
            img = base64.b64encode(img.read())
        else:
            img = ""

        description = request.data["description"]
        context = {
            'description': description,
            'img': img
        }
        configs = {
            'Template': 'Mail/bug-mail.html',
            'subject': 'Bug reportado',
            'to': ['andrescercal@hotmail.com', 'andres_f.cerquera@uao.edu.co'],
        }
        send_mail_with_file(configs, context)
        return Response({"Detail": "Bug reported"}, status=200)

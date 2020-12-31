from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from Apps.ManageBarters.models import Barter, BarterAbout, BarterSkill, BarterMode, BarterInterest
from Apps.ManageUsers.models import Area
from COCO.functions import get_place


class BarterApi(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        barter = self.create_barter(request)
        self.create_barter_about(request, barter)
        self.create_barter_skill(request, barter)
        self.create_barter_interest(request, barter)
        return Response({'Detail': 'new barter created succesfuly'},status=200)

    def create_barter(self, request):
        title = request.data['title']
        user = request.user
        return Barter.objects.create(user=user, barter_title=title)

    def create_barter_about(self, request, barter):
        description = request.data['description']
        country = request.data['country']
        city = request.data['city']
        place = get_place(country=country, city=city)
        BarterAbout.objects.create(description=description, place=place, barter=barter)

    def create_barter_skill(self, request, barter):
        skill = request.data['skill']
        area = self.get_area(area=skill)
        if area.exists():
            BarterSkill.objects.create(area=area[0], barter=barter)

    def create_barter_interest(self, request, barter):
        interest = request.data['interest']
        area = self.get_area(area=interest)
        if area.exists():
            BarterInterest.objects.create(area=area[0], barter=barter)

    def create_barter_mode(self, request, barter):
        mode = request.data['mode']
        BarterMode.objects.create(mode=mode, barter=barter)

    def get_area(self, area):
        return Area.objects.filter(area=area)

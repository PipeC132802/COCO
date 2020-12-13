from rest_framework import serializers

from Apps.ManageUsers.models import Area, UserAbout


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['area']


class UserAboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserAbout
        fields = ['bio', 'birthday', 'gender']

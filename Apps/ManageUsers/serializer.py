from rest_framework import serializers

from Apps.ManageUsers.models import Area


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = ['area']


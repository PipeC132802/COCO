from rest_framework import serializers

from Apps.ManageBarters.models import BarterComment
from Apps.ManageUsers.models import Area, UserAbout


class BarterCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterComment
        fields = ['barter', 'user_from', 'comment', 'accepted', 'photo']

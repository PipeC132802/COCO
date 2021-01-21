from rest_framework import serializers
from Apps.ManageBarters.models import BarterComment


class BarterCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = BarterComment
        fields = ['barter', 'user_from', 'comment', 'accepted', 'photo']

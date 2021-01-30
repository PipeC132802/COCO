from rest_framework import serializers

from .models import *


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'responsibility', 'respect', 'communication', 'opinion', 'created', 'user_to', 'user_from']


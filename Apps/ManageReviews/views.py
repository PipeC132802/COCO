from django.db.models import Count, Avg
from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from rest_framework.response import Response

from Apps.ManageReviews.models import Review
from Apps.ManageReviews.serializer import ReviewSerializer
from COCO.functions import get_profile_url


class ReviewsListApi(generics.RetrieveAPIView):
    model = Review

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.filter(user_to__username=self.request.GET['user'], user_to__is_active=True).order_by(
            '-created')

        reviews_list = [self.review_serializer(review=review) for review in reviews]
        return Response(reviews_list, status=200)

    @staticmethod
    def review_serializer(review):
        return {
            'id': review.pk,
            'responsibility': review.responsibility,
            'respect': review.respect,
            'communication': review.communication,
            'opinion': review.opinion,
            'user_from': {
                'username': review.user_from.username,
                'name': '{0} {1}'.format(review.user_from.first_name, review.user_from.last_name),
                'profile_profile': get_profile_url(review.user_from)
            },
            'created': review.created
        }


class ReviewsOverview(generics.RetrieveAPIView):

    def get(self, request, *args, **kwargs):
        reviews = Review.objects.filter(user_to__username=self.request.GET['user'], user_to__is_active=True).aggregate(
            responsibility=Avg('responsibility'), respect=Avg('respect'), communication=Avg('communication'),
            total=Count('id'))
        reviews['average'] = (reviews['responsibility'] + reviews['respect'] + reviews['communication']) / 3
        return Response(reviews)

    @staticmethod
    def review_overview_serializer(reviews):
        return {
            'total': reviews['total'],
            'responsibility': reviews['responsibility'],
            'respect': reviews['respect'],
            'communication': reviews['communication'],
            'average': (reviews['responsibility'] + reviews['respect'] + reviews['communication']) / 3,
        }

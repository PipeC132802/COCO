from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Review(models.Model):
    user_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_review')
    user_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_reviewed')
    responsibility = models.IntegerField()
    respect = models.IntegerField()
    communication = models.IntegerField()
    opinion = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)

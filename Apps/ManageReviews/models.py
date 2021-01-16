from django.db import models


# Create your models here.
class Review(models.Model):
    responsibility = models.IntegerField()
    respect = models.IntegerField()
    communication = models.IntegerField()
    detailed = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
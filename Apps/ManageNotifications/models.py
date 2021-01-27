from django.contrib.auth.models import User
from django.db import models


class NotificationsPreference(models.Model):
    push = models.BooleanField(default=True)
    email = models.BooleanField(default=True)
    sms = models.BooleanField(default=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' notifications preferences'

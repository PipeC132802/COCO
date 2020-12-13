from django.core.signals import request_finished
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from Apps.ManageUsers.models import UserOnline, UserPasswordChanged, UserSettings


@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserOnline.objects.create(user=instance)
        UserPasswordChanged.objects.create(user=instance)
        UserSettings.objects.create(user=instance)




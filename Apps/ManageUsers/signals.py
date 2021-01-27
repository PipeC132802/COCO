from django import dispatch
from allauth.account.signals import user_logged_in
from django.contrib.sessions.models import Session
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User

from Apps.ManageNotifications.models import NotificationsPreference
from Apps.ManageUsers.models import UserOnline, UserPasswordChanged, UserSettings, UserSession



retrieve_barters = dispatch.Signal(providing_args=[
    'request'
])

@receiver(post_save, sender=User)
def create_user_status(sender, instance, created, **kwargs):
    if created:
        UserOnline.objects.create(user=instance)
        UserPasswordChanged.objects.create(user=instance)
        UserSettings.objects.create(user=instance)
        NotificationsPreference.objects.create(user=instance)

def user_reload_page(sender, session, **kwargs):
    print(session.session_key)

retrieve_barters.connect(user_reload_page)

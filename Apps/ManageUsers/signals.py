from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from Apps.ManageUsers.models import VerifyUser


@receiver(pre_save, sender=VerifyUser)
def send_confirmation_mail(sender, instance, created, **kwargs):
    print('se ejecuta el signal')
    print(sender,'<sender')
    print(instance, '<instance')
    print('kwargs>',**kwargs)

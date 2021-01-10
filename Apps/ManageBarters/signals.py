from django.db.models.signals import post_save
from django.dispatch import receiver

from Apps.ManageBarters.models import BarterComment


@receiver(post_save, sender=BarterComment)
def create_chat(sender, instance, created, **kwargs):
    if not created and sender.accepted:
        print('creando chat...')

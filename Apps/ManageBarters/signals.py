from django.db.models.signals import post_save
from django.dispatch import receiver

from Apps.ManageBarters.models import BarterComment, Barter, BarterView


@receiver(post_save, sender=BarterComment)
def create_chat(sender, instance, created, **kwargs):
    if not created and sender.accepted:
        print('creando chat...')\

@receiver(post_save, sender=Barter)
def create_views_counter(sender, instance, created, **kwargs):
    if created:
        BarterView.objects.get_or_create(barter_id=instance.pk)

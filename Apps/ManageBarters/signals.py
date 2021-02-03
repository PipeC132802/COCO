from django.db.models import Q
from django.db.models.signals import post_save
from Apps.ManageBarters.models import Barter, BarterView
from Apps.ManageChats.models import Conversation
from django import dispatch
from django.dispatch import receiver


@receiver(post_save, sender=Barter)
def create_views_counter(sender, instance, created, **kwargs):
    if created:
        BarterView.objects.get_or_create(barter_id=instance.pk)


proposal_accepted = dispatch.Signal(providing_args=[
    'owner', 'opponent'
])


@receiver(proposal_accepted, dispatch_uid='create_chat')
def create_chat(sender, **kwargs):
    owner = kwargs.pop('owner', None)
    opponent = kwargs.pop('opponent', None)
    conversation = Conversation.objects.filter(Q(owner=owner, opponent=opponent) | Q(opponent=owner, owner=opponent))
    if not conversation.exists():
        Conversation.objects.create(owner=owner, opponent=opponent)

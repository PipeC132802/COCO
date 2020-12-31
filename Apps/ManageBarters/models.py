from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify

from Apps.ManageUsers.models import Place, Area


class Barter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    barter_title = models.CharField(max_length=225)
    slug = models.SlugField(blank=False, max_length=1024)
    edit = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.barter_title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.barter_title)
        super(Barter, self).save(*args, **kwargs)

    class Meta:
        ordering = ('-created',)


class BarterAbout(models.Model):
    description = models.TextField()
    place = models.ForeignKey(Place, on_delete=models.CASCADE)
    barter = models.OneToOneField(Barter, on_delete=models.CASCADE)

    def serializer(self):
        return {
            'description': self.description,
            'place': self.place.__str__()
        }

class BarterMode(models.Model):
    mode_statuses = (
        (1, 'Virtual'),
        (2, 'Presencial'),
    )
    mode = models.IntegerField(verbose_name="Mode", choices=mode_statuses)
    barter = models.ForeignKey(Barter, on_delete=models.CASCADE)


class BarterReaction(models.Model):
    reaction_statuses = (
        (0, 'None'),
        (1, 'Cool!'),
        (2, '¡Genial!'),
        (3, '¡Interesante!'),
    )
    reaction = models.IntegerField(verbose_name="Reaction", choices=reaction_statuses)
    barter = models.ForeignKey(Barter, on_delete=models.CASCADE)


class BarterComment(models.Model):
    def comment_directory_path(instance, filename):
        filename = 'commment_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'comments/{0}'.format(filename + ".jpg")

    comment = models.TextField()
    barter = models.ForeignKey(Barter, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=comment_directory_path, blank=True, null=True)


class BarterSkill(models.Model):
    barter = models.OneToOneField(Barter, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)


class BarterInterest(models.Model):
    barter = models.OneToOneField(Barter, on_delete=models.CASCADE)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)

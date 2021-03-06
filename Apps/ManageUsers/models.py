from datetime import datetime

from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.db import models

from COCO.settings import DOMAIN


class UserOnline(models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    is_online = models.BooleanField(default=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        message = self.user.username
        message += ' is Online' if self.is_online else ' is Offline'
        return message


class UserAbout(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField()
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=10)

    def __str__(self):
        return 'About ' + self.user.username

    def serializer(self):
        try:
            profile_picture = DOMAIN + UserProfilePhoto.objects.get(user=self.user).profile_picture.url
        except:
            profile_picture = ''
        try:
            birthday = self.birthday.strftime("%d de %b. de %Y")
        except:
            birthday = ''
        return {
            'user': self.user.username,
            'name': '{0} {1}'.format(self.user.first_name, self.user.last_name),
            'profile_picture': profile_picture,
            'bio': self.bio,
            'birthday': birthday,
            'gender': self.gender
        }


class UserProfilePhoto(models.Model):
    def user_directory_path(instance, filename):
        filename = 'user_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'profile_pictures/{0}'.format(filename + ".jpg")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return "@" + self.user.username + "'s profile picture"


class UserCoverPhoto(models.Model):
    def user_directory_path(instance, filename):
        filename = 'user_{0}'.format(datetime.now().strftime("%Y-%m-%d-%H-%M-%S%f"))
        return 'cover_photos/{0}'.format(filename + ".jpg")

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    photo = models.ImageField(upload_to=user_directory_path, blank=True)

    def __str__(self):
        return "@" + self.user.username + "'s cover photo"


class UserPasswordChanged(models.Model):
    modified = models.DateField(auto_now=True)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE
                                )

    def __str__(self):
        return self.user.username + ' cambió su contraseña el ' + str(self.modified)


class Place(models.Model):
    country = models.CharField(verbose_name="País", max_length=15)
    city = models.CharField(verbose_name="Ciudad", max_length=15)

    def __str__(self):
        return self.city + ", " + self.country


class UserContact(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    cellphone = models.CharField(max_length=20)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' vive en ' + self.place.__str__()

    def serializer(self):
        return {
            'user': self.user.username,
            'place': self.place.__str__()
        }


class Area(models.Model):
    area = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.area


class UserSkill(models.Model):
    user = models.ForeignKey(User, related_name='User_skill', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='Area_to_skill', on_delete=models.CASCADE)

    def __str__(self):
        return '@' + self.user.username + ': ' + self.area.area


class UserInterest(models.Model):
    user = models.ForeignKey(User, related_name='User_Interest', on_delete=models.CASCADE)
    area = models.ForeignKey(Area, related_name='Area_to_Interest', on_delete=models.CASCADE)

    def __str__(self):
        return '@' + self.user.username + ': ' + self.area.area


class UserRelationship(models.Model):
    relationship_statuses = (
        (0, 'None'),
        (1, 'Following'),
        (2, 'Blocked'),
    )
    user_from = models.ForeignKey(User,
                                  related_name='rel_from_set',
                                  on_delete=models.CASCADE)
    user_to = models.ForeignKey(User,
                                related_name='rel_to_set',
                                on_delete=models.CASCADE)

    created = models.DateTimeField(verbose_name='Seguido el', auto_now_add=True, db_index=True)
    status = models.IntegerField(verbose_name="Follow", choices=relationship_statuses)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
        return '{0} to {1}: {2}'.format(self.user_from.username, self.user_to.username, self.status)


class UserSettings(models.Model):
    notifications = models.BooleanField(default=True)
    include_user_in_search = models.BooleanField(default=True)
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username + ' notifications: {0}, searchs: {1}'.format(self.notifications,
                                                                               self.include_user_in_search)


class VerifyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    verified = models.BooleanField(default=False)
    token = models.CharField(max_length=50)

    def __str__(self):
        return 'token de: @' + self.user.username


class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)

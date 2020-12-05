from django.contrib import admin
from .models import *


admin.site.register(UserOnline)
admin.site.register(UserProfilePhoto)
admin.site.register(UserPasswordChanged)
admin.site.register(UserPlace)
admin.site.register(UserSkill)
admin.site.register(UserInterest)
admin.site.register(UserRelationship)


from django.contrib import admin

from Apps.ManageBarters.models import *

admin.site.register(Barter)
admin.site.register(BarterAbout)
admin.site.register(BarterMode)
admin.site.register(BarterReaction)
admin.site.register(BarterComment)
admin.site.register(BarterSkill)
admin.site.register(BarterInterest)
admin.site.register(BarterView)


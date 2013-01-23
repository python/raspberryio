from django.contrib import admin
from raspberryio.userprofile import models as userprofile


class ProfileAdmin(admin.ModelAdmin):
    model = userprofile.Profile


admin.site.register(userprofile.Profile, ProfileAdmin)

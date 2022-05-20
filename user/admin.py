from django.contrib import admin

# Register your models here.

from user.models import Profile, Fiche

admin.site.register(Profile)
admin.site.register(Fiche)
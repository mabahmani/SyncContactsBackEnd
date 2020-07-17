from django.contrib import admin

# Register your models here.
from contactApp.models import AppUser, AppContacts

admin.site.register(AppUser)
admin.site.register(AppContacts)

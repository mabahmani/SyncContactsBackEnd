from django.db import models


class AppUser(models.Model):
    app_user_phone = models.CharField(max_length=16, unique=True, null=False)
    register_token = models.TextField(null=False)

    def __str__(self):
        return self.app_user_phone


class AppContacts(models.Model):
    app_contact_phone = models.CharField(max_length=16, unique=True, null=False)
    app_users = models.ManyToManyField('AppUser')

    def __str__(self):
        return self.app_contact_phone

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_member', False)
        return super().create_superuser(username, email, password, **extra_fields)


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=True)
    objects = CustomUserManager()

    class Meta:
        app_label = 'usermanagement_24782037'

    def __str__(self):
        return self.username

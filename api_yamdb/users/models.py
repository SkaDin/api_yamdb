from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None,
                         **extra_fields):
        extra_fields.setdefault('role', 'admin')
        extra_fields.setdefault('is_verified', True)
        return super().create_superuser(username, email, password,
                                        **extra_fields)


class User(AbstractUser):
    USER_ROLES = (
        settings.USER_ROLES if hasattr(settings, 'USER_ROLES')
        else {'USER': 'user'})

    ROLE_CHOICES = ((value, role.capitalize()) for role, value in
                    USER_ROLES.items())

    email = models.EmailField(blank=False, max_length=254)
    role = models.CharField(choices=ROLE_CHOICES,
                            default=USER_ROLES.get('USER'), max_length=50)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(blank=True, null=True)
    objects = CustomUserManager()

    @property
    def is_admin(self):
        return self.role == self.USER_ROLES.get('ADMIN', 'USER')

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLES.get('MODERATOR', 'USER')

    @property
    def is_user(self):
        return self.role == self.USER_ROLES.get('USER')

    class Meta:
        ordering = ['username', ]

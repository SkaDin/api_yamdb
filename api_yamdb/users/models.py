from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db import models


class User(AbstractUser):
    USER_ROLES = (
        settings.USER_ROLES if hasattr(settings, 'USER_ROLES')
        else {'USER': 3})

    ROLE_CHOICES = ((value, role.capitalize()) for role, value in
                    USER_ROLES.items())

    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES,
                                            default=USER_ROLES.get('USER'))
    is_verified = models.BooleanField(default=False)

    @property
    def is_admin(self):
        return self.role == self.USER_ROLES.get('ADMIN', 'USER')

    @property
    def is_moderator(self):
        return self.role == self.USER_ROLES.get('MODERATOR', 'USER')

    @property
    def is_user(self):
        return self.role == self.USER_ROLES.get('USER')

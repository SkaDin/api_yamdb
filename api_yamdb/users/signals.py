from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.conf import settings
from rest_framework.authtoken.models import Token

User = get_user_model()


@receiver(post_save, sender=User)
def send_email(sender, instance, created, **kwargs):
    if created:
        print(sender.is_admin)
        email_from = settings.EMAIL_HOST_USER
        confirmation_code = Token.objects.create(user=instance)
        instance.email_user('Verification Code',
                            f'Here is verification code: {confirmation_code}',
                            email_from)

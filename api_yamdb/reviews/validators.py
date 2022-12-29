from django.core.exceptions import ValidationError
from django.utils import timezone


def validator_year(value):
    if not (0 < value <= timezone.now().year):
        raise ValidationError('Проверьте год произведения!')

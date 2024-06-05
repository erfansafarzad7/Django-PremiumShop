from django.core.exceptions import ValidationError
import re


def phone_number_validation(value):
    pattern = r'^09\d{9}$'
    if not re.match(pattern, value):
        raise ValidationError('Enter a valid phone number.')
    return True

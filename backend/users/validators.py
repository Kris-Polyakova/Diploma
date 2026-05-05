import re
from django.core.exceptions import ValidationError

def validate_username(value):

    if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
        raise ValidationError(
            'Логин должен начинаться с буквы, содержать только латинские буквы и цифры, '
            'длина от 4 до 20 символов.'
        )
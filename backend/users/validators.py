import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_username(value):
    if not re.match(r'^[a-zA-Z][a-zA-Z0-9]{3,19}$', value):
        raise ValidationError(
            'Логин должен начинаться с буквы, содержать только латинские буквы и цифры, '
            'длина от 4 до 20 символов.'
        )

def validate_password_strength(password):
    if len(password) < 6:
        raise ValidationError(_("Пароль должен содержать минимум 6 символов."))

    if not re.search(r'[A-Z]', password):
        raise ValidationError(_("Пароль должен содержать хотя бы одну заглавную букву."))

    if not re.search(r'[0-9]', password):
        raise ValidationError(_("Пароль должен содержать хотя бы одну цифру."))

    if not re.search(r'[!@#$%^&*()_+\-=\[\]{}|;:,.<>/?`~]', password):
        raise ValidationError(_("Пароль должен содержать хотя бы один специальный символ."))
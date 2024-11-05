import re
from rest_framework.serializers import ValidationError

from .constants import USERNAME_PATTERN


def username_validator(value):
    if not re.match(USERNAME_PATTERN, value):
        raise ValidationError(
            'Имя пользователя содержит недопустимые символы.')

    if value.lower() == 'me':
        raise ValidationError(
            'Имя пользователя "me" использовать запрещено.')
    return value

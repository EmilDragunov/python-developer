from django.contrib.auth.models import AbstractUser
from django.db import models

from api.users.constants import (MAX_LENGTH_CHAR_FIELD,
                                 MAX_LENGTH_USERNAME_FIELD,
                                 MAX_LENGTH_EMAIL_FIELD,
                                 MAX_LENGTH_ROLE_FIELD)

USER = 'user'
MODERATOR = 'moderator'
ADMIN = 'admin'

ROLES = [
    ('user', USER),
    ('moderator', MODERATOR),
    ('admin', ADMIN),
]


class User(AbstractUser):
    """Модель пользователя."""

    username = models.CharField(
        verbose_name='Логин пользователя',
        unique=True,
        max_length=MAX_LENGTH_USERNAME_FIELD,
    )
    email = models.EmailField(
        verbose_name='eMail пользователя',
        unique=True,
        max_length=MAX_LENGTH_EMAIL_FIELD,
    )
    first_name = models.CharField(
        verbose_name='Имя пользователя',
        blank=True,
        max_length=MAX_LENGTH_CHAR_FIELD,
    )
    last_name = models.CharField(
        verbose_name='Фамилия пользователя',
        blank=True,
        max_length=MAX_LENGTH_CHAR_FIELD,
    )
    bio = models.TextField(
        verbose_name='Биография пользователя',
        blank=True,
    )
    role = models.CharField(
        verbose_name='Роль пользователя',
        choices=ROLES,
        default=USER,
        blank=True,
        max_length=MAX_LENGTH_ROLE_FIELD,
    )
    confirmation_code = models.SlugField(
        verbose_name='Код подтверждения',
        null=True,
        blank=True
    )

    @property
    def is_admin(self):
        return self.role == ADMIN or self.is_staff or self.is_superuser

    @property
    def is_moderator(self):
        return self.role == MODERATOR

    class Meta:
        ordering = ('username',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username

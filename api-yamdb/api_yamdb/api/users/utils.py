from django.core.mail import send_mail

from api_yamdb import settings


def send_email(user_email, confirmation_code):
    """Отправка кода подтверждения по email."""
    send_mail(
        'Код подтверждения',
        f'Ваш код подтверждения - {confirmation_code}',
        settings.EMAIL_FROM,
        [user_email]
    )

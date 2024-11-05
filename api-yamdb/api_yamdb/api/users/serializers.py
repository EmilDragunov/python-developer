from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import User
from .constants import MAX_LENGTH_USERNAME_FIELD, MAX_LENGTH_EMAIL_FIELD
from .validators import username_validator
from rest_framework.serializers import ValidationError


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для регистрации."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_USERNAME_FIELD,
        validators=(username_validator, )
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL_FIELD,
    )

    class Meta:
        model = User
        fields = ('username', 'email')

    def create(self, validated_data):
        user, created = User.objects.get_or_create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
        )

        return user

    def validate(self, data):
        username = data.get('username')
        email = data.get('email')

        if User.objects.filter(username=username, email=email).exists():
            return data
        if User.objects.filter(username=username).exists():
            raise ValidationError('Этот логин уже занят')
        if User.objects.filter(email=email).exists():
            raise ValidationError('Этот email уже используется')

        return data


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователя."""

    username = serializers.CharField(
        required=True,
        max_length=MAX_LENGTH_USERNAME_FIELD,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message="Этот логин уже занят"),
            username_validator,
        ]
    )
    email = serializers.EmailField(
        required=True,
        max_length=MAX_LENGTH_EMAIL_FIELD,
        validators=[
            UniqueValidator(queryset=User.objects.all(),
                            message="Этот email уже используется")
        ]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role')


class UserMeSerializer(UserSerializer):
    """Сериализатор для me"""

    class Meta(SignUpSerializer.Meta):
        model = User
        fields = (
            'username', 'email',
            'first_name', 'last_name',
            'bio', 'role'
        )


class TokenSerializer(serializers.Serializer):
    """Сериализатор для получения токена."""

    username = serializers.CharField(required=True)
    confirmation_code = serializers.CharField(required=True)

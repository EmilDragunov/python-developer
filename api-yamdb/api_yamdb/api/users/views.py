from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.generics import get_object_or_404
from django.contrib.auth.tokens import default_token_generator

from users.models import User
from api.permissions import IsAdmin
from .serializers import (SignUpSerializer, TokenSerializer,
                          UserSerializer, UserMeSerializer)
from .utils import send_email


class UserViewSet(viewsets.ModelViewSet):
    """Управление пользователями."""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin)
    filter_backends = [SearchFilter]
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'head', 'patch', 'delete')

    @action(
        methods=['get'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        serializer_class=UserSerializer,
    )
    def me(self, request):
        serializer = UserMeSerializer(
            self.request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )

    @me.mapping.patch
    def patch_me(self, request):
        serializer = UserMeSerializer(
            self.request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.validated_data.pop('role', None)
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    """Регистрация."""
    serializer = SignUpSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    confirmation_code = default_token_generator.make_token(user)

    send_email(
        user_email=user.email,
        confirmation_code=confirmation_code,
    )

    return Response(
        serializer.validated_data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    """Генерация токена."""
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = get_object_or_404(
        User,
        username=request.data.get('username'),
    )
    if not default_token_generator.check_token(
            user,
            request.data.get('confirmation_code'),
    ):
        return Response(
            'Неверный токен',
            status=status.HTTP_400_BAD_REQUEST,
        )

    token = AccessToken.for_user(user)

    return Response(
        {'token': str(token)},
        status=status.HTTP_200_OK,
    )

from rest_framework.filters import SearchFilter
from api.permissions import IsAdminOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import (ListModelMixin, CreateModelMixin,
                                   DestroyModelMixin,)
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class CategoryGenreMixin(
    ListModelMixin,
    CreateModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    lookup_field = 'slug'
    filter_backends = [SearchFilter]
    search_fields = ['name']
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly)


class HttpMethodMixin:
    http_method_names = ['get', 'post', 'patch', 'delete']

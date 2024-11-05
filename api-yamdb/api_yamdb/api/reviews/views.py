from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from reviews.models import (Title, Category, Genre,
                            Review)
from .serializers import (CategorySerializer, GenreSerializer,
                          TitleWriteSerializer, TitleReadSerializer,
                          ReviewSerializer, CommentSerializer)
from rest_framework.generics import get_object_or_404
from api.permissions import (IsAdminOrReadOnly,
                             IsOwnerOrModeratorOrAdminOrReadOnly)
from django_filters.rest_framework import DjangoFilterBackend
from .filters import TitleFilter
from .mixins import CategoryGenreMixin, HttpMethodMixin


class TitleViewSet(HttpMethodMixin, viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TitleReadSerializer
        return TitleWriteSerializer


class CategoryViewSet(CategoryGenreMixin):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(CategoryGenreMixin):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class ReviewViewSet(HttpMethodMixin, viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrModeratorOrAdminOrReadOnly
    )

    @property
    def title_object(self):
        return get_object_or_404(Title, id=self.kwargs['title_id'])

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.title_object)

    def get_queryset(self):
        return self.title_object.reviews.all()


class CommentViewSet(HttpMethodMixin, viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthenticatedOrReadOnly,
        IsOwnerOrModeratorOrAdminOrReadOnly
    )

    @property
    def review_object(self):
        return get_object_or_404(Review, id=self.kwargs['review_id'],
                                 title_id=self.kwargs.get('title_id'))

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.review_object)

    def get_queryset(self):
        return self.review_object.comments.all()

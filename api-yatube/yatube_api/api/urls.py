from django.urls import path, include
from rest_framework.routers import DefaultRouter
from api.views import (PostViewSet, GroupViewSet,
                       CommentViewSet, UserViewSet,
                       FollowViewSet)


router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')
router.register('groups', GroupViewSet, basename='groups')
router.register(r'posts/(?P<post_id>\d+)/comments', CommentViewSet,
                basename='comments')
router.register('users', UserViewSet, basename='users')
router.register('follow', FollowViewSet, basename='follow')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.jwt')),
]

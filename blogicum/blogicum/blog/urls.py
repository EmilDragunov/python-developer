from django.urls import path
from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.EndpointPostListView.as_view(),
         name='endpoint'),
    path('posts/<int:post_id>/', views.PostDetailView.as_view(),
         name='post_detail'),
    path('category/<slug:category_slug>/', views.CategoryListView.as_view(),
         name='category_posts'),
    path('profile/<str:username>/', views.ProfileDetailView.as_view(),
         name='profile'),
    path('profile/<str:username>/edit/', views.ProfileUpdateView.as_view(),
         name='edit_profile'),
    path('posts/create/', views.PostCreateView.as_view(),
         name='create_post'),
    path('posts/<int:post_id>/edit/', views.PostUpdateView.as_view(),
         name='edit_post'),
    path('posts/<int:post_id>/delete/', views.PostDeleteView.as_view(),
         name='delete_post'),
    path('posts/<int:post_id>/comment/', views.CommentCreateView.as_view(),
         name='add_comment'),
    path('posts/<int:post_id>/edit_comment/<int:comment_id>/',
         views.CommentUpdateView.as_view(),
         name='edit_comment'),
    path('posts/<int:post_id>/delete_comment/<int:comment_id>/',
         views.CommentDeleteView.as_view(),
         name='delete_comment'),
]

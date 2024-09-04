from django.contrib import admin
from django.urls import path
from .views import AllPostsAPIView, CreatePostAPI, UpdatePostAPI, LikePostAPIView, DislikePostAPIView

urlpatterns = [
    path('posts/', AllPostsAPIView.as_view({'get': 'list'}), name='api_all_posts'),
    path('post/', CreatePostAPI.as_view(), name='create_post_api'),
    path('post/<int:pk>/', UpdatePostAPI.as_view(), name='edit_post_api'),
    # path('post/<int:pk>/', PostDeleteView.as_view(), name='delete_post_api'),
    path('posts/like/<int:pk>/', LikePostAPIView.as_view(), name='like_post_api'),
    path('posts/dislike/<int:pk>/', DislikePostAPIView.as_view(), name='dislike_post_api'),
]
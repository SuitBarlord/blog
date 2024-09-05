from django.contrib import admin
from django.urls import path
from .views import PostList, UpdatePostAPI, LikePostAPIView, DislikePostAPIView

urlpatterns = [
    path('posts/', PostList.as_view(), name='api_all_posts'),
    path('post/', PostList.as_view(), name='create_post_api'),
    path('post/<int:pk>/', UpdatePostAPI.as_view(), name='edit_post_api'),
    path('post/<int:pk>/', UpdatePostAPI.as_view(), name='delete_post_api'),
    path('post/like/<int:pk>/', LikePostAPIView.as_view(), name='like_post_api'),
    path('post/dislike/<int:pk>/', DislikePostAPIView.as_view(), name='dislike_post_api'),
]
from django.contrib import admin
from django.urls import path
from .views import AllPostsView, CreatePost, EditPost, DeletePost, like_post

urlpatterns = [
    path('', AllPostsView.as_view(), name='all_posts_view'),  
    path('create_post/', CreatePost.as_view(), name='create_post'),  
    path('edit_post/<int:pk>/', EditPost.as_view(), name='edit_post'),  
    path('delete_post/<int:pk>/', DeletePost.as_view(), name='delete_post'),  
    path('like_post/<int:post_id>/', like_post, name='like_post'),
]
from rest_framework import serializers
from posts.models import Post

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['topic', 'content', 'author']  # Указываем только те поля, которые пользователь может указать при создании записи


class EditPostSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField()
    class Meta:
        model = Post
        fields = ['id', 'topic', 'content', 'author']


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'topic', 'content', 'number_likes', 'author']
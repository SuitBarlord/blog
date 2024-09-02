from posts.models import Post
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from posts.models import Post
from .serializers import PostSerializer, PostCreateSerializer, EditPostSerializer, LikePostSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin
# Create your views here.


class AllPostsAPIView(PermissionRequiredMixin, viewsets.ModelViewSet):
    permission_required = 'posts.view_post'
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    

class CreatePostAPI(PermissionRequiredMixin, APIView):
    permission_required = 'posts.add_post'
    def post(self, request):
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class UpdatePostAPI(PermissionRequiredMixin, APIView):
    permission_required = 'posts.change_post'
    def put(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = EditPostSerializer(instance=post, data=request.data, partial=True)

        if serializer.is_valid():
            new_id = request.data['id']
            
            print(new_id)
            # Проверка, есть ли запись с таким id 
            if Post.objects.filter(id=new_id).exists() and new_id != pk:
                return Response({'error': 'Запись с указанным ID уже существует'}, status=status.HTTP_400_BAD_REQUEST)

            post.topic = serializer.validated_data.get('topic', post.topic)
            post.content = serializer.validated_data.get('content', post.content)
            post.author = serializer.validated_data.get('author', post.author)
            post.id = new_id
            post.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class PostDeleteView(PermissionRequiredMixin, APIView):
    permission_required = 'posts.delete_post'
    #  PostSerializer используется для сериализации сообщения в JSON
    #  После сериализации вызывается метод delete() для удаления сообщения
    #  Сериализованные данные возвращаются в качестве ответа, чтобы клиент мог подтвердить успешное удаление
    def delete(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)

        post.delete()
        # успешный ответ.
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LikePostAPIView(PermissionRequiredMixin, APIView):
    permission_required = 'posts.view_post'
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = LikePostSerializer(post)


        if Post.objects.filter(pk=pk).exists() == True:
            post.number_likes += 1

            post.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DislikePostAPIView(PermissionRequiredMixin, APIView):
    permission_required = 'posts.view_post'
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)
        serializer = LikePostSerializer(post)


        if Post.objects.filter(pk=pk).exists() == True:
            if post.number_likes == 0:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            else:
                post.number_likes -= 1

                post.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
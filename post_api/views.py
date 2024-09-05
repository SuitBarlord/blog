from posts.models import Post
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from .serializers import PostSerializer, PostCreateSerializer, EditPostSerializer, LikePostSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import CustomUser
from .services import post_list_service, update_post_service, like_post_service
# Create your views here.



class PostList(APIView):

    def get(self, request):
        # Переделал проверку прав так как использовал get  и post в совокупности в обном представлении
        # Теперь проверка прав без миксинов а через has_perm
        if not request.user.has_perm('posts.view_post'):
            return Response({'message': 'У вас нет прав доступа для просмотра'}, status=status.HTTP_403_FORBIDDEN)

        posts = post_list_service.get_all_posts()
        return Response(posts, status=status.HTTP_200_OK)


    def post(self, request):
        if not request.user.has_perm('posts.add_post'):
            return Response({'message': 'У вас нет прав доступа для создания записей'}, status=status.HTTP_403_FORBIDDEN)

        data = request.data
        new_post = post_list_service.create_post(data)
        if 'errors' in new_post:
            return Response(new_post, status=status.HTTP_400_BAD_REQUEST)
        return Response(new_post, status=status.HTTP_201_CREATED)


class UpdatePostAPI(APIView):

    def put(self, request, pk):
        if not request.user.has_perm('posts.change_post'):
            return Response({'message': 'У вас нет прав доступа для редактирования'}, status=status.HTTP_403_FORBIDDEN)
        
        post = update_post_service.update_post(request, pk)

        if 'errors' in post:
            return Response(post, status=status.HTTP_400_BAD_REQUEST)
        return Response(post.data, status=status.HTTP_200_OK)

    
    def delete(self, request, pk):
        if not request.user.has_perm('posts.delete_post'):
            return Response({'message': 'У вас нет прав доступа для удаления'}, status=status.HTTP_403_FORBIDDEN)

        serializer = update_post_service.delete_post(pk)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class LikePostAPIView(PermissionRequiredMixin, APIView):
    permission_required = 'posts.view_post'
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)

        # Сделал просто проверку уже ранее запрошенной записи
        if post != None:
            serializer = like_post_service.like_post(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class DislikePostAPIView(PermissionRequiredMixin, APIView):
    permission_required = 'posts.view_post'
    def get(self, request, pk):
        post = Post.objects.get(pk=pk)

        # Сделал просто проверку уже ранее запрошенной записи
        if post != None:
            serializer = like_post_service.dislike_post(post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


    
from posts.models import Post
from .serializers import PostSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from posts.models import Post
from .serializers import PostSerializer, PostCreateSerializer, EditPostSerializer, LikePostSerializer
from django.contrib.auth.mixins import PermissionRequiredMixin
from users.models import CustomUser
# Create your views here.



class PostList(APIView):

    def get(self, request):
        # Переделал проверку прав так как использовал get  и post в совокупности в обном представлении
        # Теперь проверка прав без миксинов а через has_perm
        if not request.user.has_perm('posts.view_post'):
            return Response({'message': 'У вас нет прав доступа для просмотра'}, status=status.HTTP_403_FORBIDDEN)

        queryset = Post.objects.all()
        serializer = PostSerializer(queryset, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if not request.user.has_perm('posts.add_post'):
            return Response({'message': 'У вас нет прав доступа для создания записей'}, status=status.HTTP_403_FORBIDDEN)

        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class UpdatePostAPI(APIView):

    def put(self, request, pk):
        if not request.user.has_perm('posts.change_post'):
            return Response({'message': 'У вас нет прав доступа для редактирования'}, status=status.HTTP_403_FORBIDDEN)
        post = Post.objects.get(pk=pk)
        serializer = EditPostSerializer(instance=post, data=request.data, partial=True)
        
        user = CustomUser.objects.get(pk=request.data['author'])
        
        if serializer.is_valid():
            new_id = request.data['id']
            
            print(new_id)
            # После установки свойства уникальности id в модели при запросе на изменение id 
            # на такой который есть, django выбьет ошибку, и не поменяет id)
            if new_id != post.id:
                Post.objects.create(id=new_id, topic=request.data['topic'],  content=request.data['content'], author=user)
                
                post.delete()
            else:

                post.topic = serializer.validated_data.get('topic', post.topic)
                post.content = serializer.validated_data.get('content', post.content)
                post.author = serializer.validated_data.get('author', post.author)
                post.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        if not request.user.has_perm('posts.delete_post'):
            return Response({'message': 'У вас нет прав доступа для удаления'}, status=status.HTTP_403_FORBIDDEN)
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)

        post.delete()

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
    


    
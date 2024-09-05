from posts.models import Post
from ..serializers import EditPostSerializer, PostSerializer
from users.models import CustomUser

def update_post(request, pk):

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

    return serializer


def delete_post(pk):

    post = Post.objects.get(pk=pk)

    serializer = PostSerializer(post)

    post.delete()

    return serializer
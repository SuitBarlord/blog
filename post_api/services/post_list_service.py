from posts.models import Post
from ..serializers import PostSerializer

def get_all_posts():
    queryset = Post.objects.all()
    serializer = PostSerializer(queryset, many=True)
    return serializer.data

def create_post(data):
    serializer = PostSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return serializer.data
    return serializer.errors
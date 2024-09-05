from ..serializers import LikePostSerializer

def like_post(post):
    post.number_likes += 1
    post.save()
    serializer = LikePostSerializer(post)
    return serializer

def dislike_post(post):
    if post.number_likes > 0:
        post.number_likes -= 1
        post.save()
        serializer = LikePostSerializer(post)
        return serializer

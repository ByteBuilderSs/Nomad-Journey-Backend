from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from blog.models import Blog
from .serializers import *
from accounts.models import User


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateLike(request, post_id):
    post = Blog.objects.get(id=post_id)
    serializer = LikePostSerializer(data=request.data, context={"request" : request, "post" : post})

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetPostsWithLike(request, post_id):
    post = Blog.objects.get(id=post_id)
    likers_ids = Like.objects.filter(post=post_id).values('liker')
    likers_objs = User.objects.filter(id__in=likers_ids)

    ref = Like.objects.filter(post=post_id).first()

    setattr(ref, 'post', post)
    setattr(ref, 'likers', likers_objs)

    serializer = PostWithLikesSerializer(ref)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteLike(request, like_id):
    like = Like.objects.get(id=like_id)
    like.delete()
    return Response('Like deleted successfully!')
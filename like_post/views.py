from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from blog.models import Blog
from .serializers import *
from accounts.models import User
from notification.models import Notification


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateLike(request, post_id):
    post = Blog.objects.get(uid=post_id)
    serializer = LikePostSerializer(data=request.data, context={"request" : request, "post" : post})

    if serializer.is_valid():
        serializer.save()

    notif = Notification.objects.create(
        user_sender=request.user,
        user_receiver=post.author,
        notif_type='like_post'
    ) 

    return Response(serializer.data)

@api_view(['GET'])
def GetPostsWithLike(request, post_id):
    likers_ids = Like.objects.filter(liked_post=post_id).values('liker')
    likers_objs = User.objects.filter(id__in=likers_ids.all())
    serializer = UserCompeleteProfileSerializer(likers_objs, many=True)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteLike(request, uid, liker):
    like = Like.objects.get(liker=liker, liked_post = uid)
    like.delete()
    return Response('Like deleted successfully!')
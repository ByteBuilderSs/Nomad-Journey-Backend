from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from blog.models import Blog
from .serializers import LikePostSerializer


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateLike(request, post_id):
    post = Blog.objects.get(id=post_id)
    serializer = LikePostSerializer(data=request.data, context={"request" : request, "post" : post})

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)
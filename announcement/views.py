from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Announcement
from .serializers import AnnouncementSerializer
from rest_framework.permissions import IsAuthenticated
from accounts.models import User


@api_view(['GET'])
def user_announcement(request, username):
    announcement = Announcement.objects.get(announcer=User.objects.get(username=username))
    serializer = AnnouncementSerializer(announcement, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAnnouncementList(request):
    announcements = Announcement.objects.all()
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAnnouncementsForHost(request):
    announcements = Announcement.objects.filter(anc_city=request.user.city).filter(anc_status='P')
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetSingleAnnouncement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    serializer = AnnouncementSerializer(announcement, many=False)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateAnnouncement(request):
    serializer = AnnouncementSerializer(data=request.data, context={"request" : request})
    
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def EditAnnouncement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    serializer = AnnouncementSerializer(instance=announcement, data=request.data)

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def DeleteAnnouncement(request, pk):
    announcement = Announcement.objects.get(id=pk)
    announcement.delete()
    return Response('Item successfully deleted!')


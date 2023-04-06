from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import AnnouncementSerializer, UnAuthAnnouncementDetailsSerializer
from .models import Announcement
from accounts.models import User
from anc_request.models import AncRequest


@api_view(['GET'])
def UserAnnouncements(request, username):
    user = User.objects.get(username=username)
    announcements = Announcement.objects.filter(announcer=user.id)
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def UserAnnouncementsMoreDetails(request, username):
    user = User.objects.get(username=username)
    announcements = Announcement.objects.filter(announcer=user.id)
    serializer = UnAuthAnnouncementDetailsSerializer(announcements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def UserAnnouncementsWithHostRequest(request, user_id):
    user = User.objects.get(username=user_id)
    announcements = Announcement.objects.filter(announcer=user.id)
    anc_ids = AncRequest.objects.filter(req_anc__in=announcements.values('id')).values('req_anc')
    final_announcements = Announcement.objects.filter(id__in=anc_ids)
    serializer = AnnouncementSerializer(final_announcements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAnnouncementsForHost(request):
    request_ids = AncRequest.objects.filter(host=request.user.id).values('req_anc')
    announcements = Announcement.objects.filter(anc_city=request.user.User_city).filter(anc_status='P')
    announcements = announcements.exclude(id__in=request_ids).exclude(announcer=request.user.id)
    serializer = AnnouncementSerializer(announcements, many=True)
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
    return Response('Announcement deleted successfully!')


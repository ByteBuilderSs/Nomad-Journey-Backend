from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import AncRequest
from .serializers import AncRequestSerializer
from announcement.models import Announcement
from accounts.models import User
from accounts.serializers import UserSerializer
from announcement.serializers import AnnouncementSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetHostsOfAnnouncement(request, anc_id):
    anc_requests = AncRequest.objects.filter(req_anc=anc_id)
    hosts = User.objects.filter(id__in=anc_requests.values('host'))
    serializer = UserSerializer(hosts, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetRequestsOfHost(request, host_id):
    anc_requests = AncRequest.objects.filter(host=host_id)
    serializer = AncRequestSerializer(anc_requests, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateRequest(request, anc_id):
    announcement = Announcement.objects.get(id=anc_id)
    serializer = AncRequestSerializer(data=request.data, context={"request" : request, "announcement" : announcement})

    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AcceptRequest(request, req_id):
    req = AncRequest.objects.get(id=req_id)
    announcement = Announcement.objects.filter(id=req.req_anc.id)
    announcement.update(anc_status='A')
    announcement.update(main_host=req.host)
    serializer = AnnouncementSerializer(data=announcement)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def RejectRequest(request, req_id):
    req = AncRequest.objects.get(id=req_id)
    req.delete()
    return Response('Request deleted successfully!')
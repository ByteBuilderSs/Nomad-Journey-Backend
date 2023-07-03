from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics , status
from .models import AncRequest
from .serializers import AncRequestSerializer
from announcement.models import Announcement
from accounts.models import User
from accounts.serializers import UserSerializer
from announcement.serializers import AnnouncementSerializer
from notification.models import Notification


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

    notif = Notification.objects.create(
        user_sender=request.user,
        user_receiver=announcement.announcer,
        notif_type='offer_to_host'
    ) 

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def AcceptRequest(request, req_id, host_id):
    req = AncRequest.objects.get(req_anc = req_id, host = host_id)
    announcement = Announcement.objects.filter(id = req.req_anc.id)
    user = User.objects.get(id = request.user.id)
    if user.coins < 2:
        return Response({
            'data': serializer.errors,
            'message':'you need more coins to accept host'
        } , status = status.HTTP_400_BAD_REQUEST)
    user.coins = user.coins - 2
    user.save()
    announcement.update(anc_status='A')
    announcement.update(main_host=req.host)
    serializer = AnnouncementSerializer(data=announcement)
    if serializer.is_valid():
        serializer.save()

    notif = Notification.objects.create(
        user_sender=request.user,
        user_receiver=host_id,
        notif_type='chosen_as_main_host'
    ) 

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def RejectRequest(request, req_id, host_id):
    req = AncRequest.objects.get(req_anc = req_id, host = host_id)
    req.delete()
    return Response('Request deleted successfully!')
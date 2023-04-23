from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import AnnouncementSerializer, UnAuthAnnouncementDetailsSerializer, FuckingAnnouncementSerializer,DoneStatusAnnouncementsSerializer
from .models import Announcement
from accounts.models import User
from anc_request.models import AncRequest
from rest_framework.pagination import PageNumberPagination
from rest_framework.settings import api_settings
import math


def SortData(data, sort_by, descending=False):
    if sort_by == 'anc_timestamp_created':
        if descending:
            return data.order_by('-anc_timestamp_created')
        else:
            return data.order_by('anc_timestamp_created')
    elif sort_by == 'arrival_date':
        if descending:
            return data.order_by('-arrival_date')
        else:
            return data.order_by('arrival_date')
    elif sort_by == 'travelers_count':
        if descending:
            return data.order_by('-travelers_count')
        else:
            return data.order_by('travelers_count')
    else:
        return 'Invalid sort request!'


@api_view(['GET'])
def UserAnnouncements(request, username):
    user = User.objects.get(username=username)
    announcements = Announcement.objects.filter(announcer=user.id)
    serializer = AnnouncementSerializer(announcements, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def UserAnnouncementsMoreDetails(request, pk):
    announcements = Announcement.objects.get(id=pk)
    serializer = UnAuthAnnouncementDetailsSerializer(announcements, many=False)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def UserAnnouncementsWithHostRequest(request, user_id):
    announcements = Announcement.objects.filter(announcer=user_id)
    requests = AncRequest.objects.filter(req_anc__in=announcements.values('id'))
    announcements_with_request = Announcement.objects.filter(id__in=requests.values('req_anc'))
    
    for anc in announcements_with_request:
        host_ids = AncRequest.objects.filter(req_anc=anc.id).values('host')
        hosts = User.objects.filter(id__in=host_ids)
        setattr(anc, 'hosts', hosts)
    serializer = FuckingAnnouncementSerializer(announcements_with_request, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAnnouncementsForHost(request):
    pagination = PageNumberPagination()

    # initial objects
    request_ids = AncRequest.objects.filter(host=request.user.id).values('req_anc')
    announcements = Announcement.objects.filter(anc_city=request.user.User_city).filter(anc_status='P')
    announcements = announcements.exclude(id__in=request_ids).exclude(announcer=request.user.id)

    # sorting
    sort_by = request.GET.get('sort_by', None)
    descending = request.GET.get('descending', False)
    if sort_by:
        announcements = SortData(announcements, sort_by, descending)

    # pagination
    page = pagination.paginate_queryset(announcements, request)
    serializer = AnnouncementSerializer(page, many=True)
    result = pagination.get_paginated_response(serializer.data)
    result.data['page_count'] = math.ceil(len(announcements) / api_settings.PAGE_SIZE)
    return result

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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAnnouncementDetailByAnnouncementId(request, ans_id):
    annuncement = Announcement.objects.get(id = ans_id)
    serializer = AnnouncementSerializer(annuncement)
    return Response(serializer.data)


@api_view(['GET'])
def GetDoneStatusAnnouncements(request, username):
    user = User.objects.get(username=username)
    announcements = Announcement.objects.filter(announcer=user.id , anc_status = 'D')
    serializer = DoneStatusAnnouncementsSerializer(announcements, many=True)
    return Response(serializer.data)
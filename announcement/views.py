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
from django.db.models import F
import datetime
from utils.views import *
from utils.models import Language


def SortData(data, sort_by, descending=False):
    if sort_by == 'anc_timestamp_created':
        if descending:
            return data.order_by('-anc_timestamp_created')
        else:
            return data.order_by('anc_timestamp_created')
    elif sort_by == 'time_range':
        if descending:
            return data.annotate(diff=F('departure_date') - F('arrival_date')).order_by('-diff')
        else:
            return data.annotate(diff=F('departure_date') - F('arrival_date')).order_by('diff')
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
    current_time = datetime.datetime.now().date()
    for a in announcements:
        if a.anc_status == 'P' and current_time > a.arrival_date:
            setattr(a , 'anc_status' , 'E')
            a.save()
        elif a.anc_status == 'A' and current_time >= a.departure_date:
            setattr(a , 'anc_status' , 'D')
            a.save()
        else:
            print(a.anc_status)
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
    announcements = Announcement.objects.filter(anc_status='P')
    announcements = announcements.exclude(id__in=request_ids).exclude(announcer=request.user.id)

    # sorting
    sort_by = request.GET.get('sort_by', None)
    descending = request.GET.get('descending', False)
    if sort_by:
        announcements = SortData(announcements, sort_by, descending)

    # filter
    city_filter_values = request.GET.get('city', None)
    country_filter_values = request.GET.get('country', None)
    start_time = request.GET.get('start_time', None)
    end_time = request.GET.get('end_time', None)
    language_filter_values = request.GET.get('language', None)

    if city_filter_values is None and country_filter_values is None:
        announcements = announcements.filter(anc_city=request.user.User_city)
    else:
        announcements_1 = None
        announcements_2 = None
        
        if city_filter_values:
            announcements_1 = announcements.filter(anc_city__city_name__in=city_filter_values.split(','))
        if country_filter_values:
            announcements_2 = announcements.filter(anc_city__country__in=country_filter_values.split(','))
        
        if announcements_1 is not None and announcements_2 is not None:
            announcements = announcements_1 | announcements_2
        elif announcements_1 is None and announcements_2 is None:
            announcements = None
        elif announcements_1 is None:
            announcements = announcements_2
        elif announcements_2 is None:
            announcements = announcements_1

    if start_time and end_time:
        start_date = datetime.datetime.strptime(start_time, '%Y-%m-%d').date()
        end_date = datetime.datetime.strptime(end_time, '%Y-%m-%d').date()
        announcements = announcements.filter(arrival_date__range=[start_date, end_date])

    if language_filter_values:
        related_users_to_langs = []
        for lang in language_filter_values.split(','):
            print(lang)
            lang_obj = Language.objects.get(id=lang)
            print(lang_obj)
            related_users_to_langs += lang_obj.langF.all().values('id')
            related_users_to_langs += lang_obj.langL.all().values('id')
        print(related_users_to_langs)
        related_announcments = []
        traversed_users = []
        for related_user in related_users_to_langs:
            print(related_user)
            if related_user in traversed_users:
                continue
            related_announcments.append(Announcement.objects.filter(announcer=related_user['id']))
            traversed_users.append(related_user)
        print(traversed_users)
        print(related_announcments)
        announcements = related_announcments

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
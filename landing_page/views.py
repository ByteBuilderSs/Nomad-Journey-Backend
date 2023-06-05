from django.shortcuts import render
from django.db.models import Avg, ExpressionWrapper, F , Q
from rest_framework.views import APIView
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from announcement.models import Announcement
from feedback.models import Feedback
from accounts.models import *
from .serializers import *
from utils.models import City
import json
from django.http import JsonResponse


class MostRatedHost(APIView):
    def get(self,request):
        avg_feedbacks = Feedback.objects.values('ans_id__main_host').annotate(
            avg_feedback=Avg(F('question_1') + F('question_2') + F('question_3') + F('question_4') + F('question_5')) / 5
        )
        avg_feedback_sorted = avg_feedbacks.order_by('-avg_feedback')
        # max_avg_feedback_value = max_avg_feedback['avg_feedback']
        announcements_query = []
        print(len(avg_feedback_sorted))
        for i in range(len(avg_feedback_sorted)):
            announcements_query.append(Announcement.objects.filter(main_host=avg_feedback_sorted[i]['ans_id__main_host']).first())
        # announcements_query = Announcement.objects.filter(main_host=max_avg_feedback['ans_id__main_host'])
        announcements = announcements_query[:10]
        serializer = MostRatedHostSerializer(announcements , many= True)
        return Response(serializer.data)

class MostVisitedCities(APIView):
    def get(self,request):
        cities_query = City.objects.annotate(num_announcements=models.Count('announcement')).order_by('-num_announcements')
        cities_with_images = cities_query.exclude(Q(city_small_image64=None) | Q(city_small_image64=True))
        cities = cities_with_images[:10]
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class RandomShit(APIView):
    def get(self, request):
        cities_query = City.objects.exclude(Q(city_big_image64=None) | Q(city_big_image64=True))
        cities = cities_query[:10]
        cities_f = []
        for c in cities:
            if c.city_name != "Sydney" and c.city_name != "Rome" :
                cities_f.append(c)
        serializer = CityRandomshitSerializer(cities_f, many=True)
        return Response(serializer.data)

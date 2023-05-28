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
        max_avg_feedback = avg_feedbacks.order_by('-avg_feedback').first()
        max_avg_feedback_value = max_avg_feedback['avg_feedback']
        announcements = Announcement.objects.filter(main_host=max_avg_feedback['ans_id__main_host'])
        data = []
        for announcement in announcements:
            avg_feedback = Feedback.objects.filter(ans_id=announcement.id).aggregate(
                avg_feedback=Avg(F('question_1') + F('question_2') + F('question_3') + F('question_4') + F('question_5')) / 5
            )
            data.append({
                'id': announcement.id,
                'announcer': announcement.announcer.username,
                'announcer_id' : announcement.announcer,
                'anc_city': announcement.anc_city.city_name,
                'arrival_date': announcement.arrival_date,
                'departure_date': announcement.departure_date,
                'travelers_count' : announcement.travelers_count,
                'avg_feedback': avg_feedback['avg_feedback'],
            })

        return JsonResponse(data, safe=False)

class MostVisitedCities(APIView):
    def get(self,request):
        cities = City.objects.annotate(num_announcements=models.Count('announcement')).order_by('-num_announcements')[:5]
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

class RandomShit(APIView):
    def get(self, request):
        cities = City.objects.exclude(Q(city_big_image64=None) | Q(city_big_image64=True))[:8]
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)

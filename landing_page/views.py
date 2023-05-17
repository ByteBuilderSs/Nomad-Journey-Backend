from django.shortcuts import render
from django.db.models import Avg, ExpressionWrapper, F
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
                'anc_city': announcement.anc_city.city_name,
                'arrival_date': announcement.arrival_date,
                'departure_date': announcement.departure_date,
                'travelers_count' : announcement.travelers_count,
                'avg_feedback': avg_feedback['avg_feedback'],
                # Add more fields as needed
            })

        return JsonResponse(data, safe=False)



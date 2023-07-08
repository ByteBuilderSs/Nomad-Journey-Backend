from django.shortcuts import render
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from announcement.models import Announcement
from .models import Feedback
from .serializers import *
import json
from accounts.models import User
from blog.models import Blog

class FeedbackViewByAncId(APIView):
    def get(self , request , anc_id):
        # try:
        feedback= Feedback.objects.filter(ans_id = anc_id)
        serializer = FeedbackSerializerToGet(feedback[0])
        return Response({
            'data':serializer.data,
            'message' : 'feedback fetched successfully'
        } , status = status.HTTP_201_CREATED)
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )

class FeedbackView(APIView):
    def get(self , request , username):
        # try:
        user_id = User.objects.get(username = username).id
        feedback= Feedback.objects.filter(user_id = user_id)
        serializer = FeedbackSerializerToGet(feedback[0])
        return Response({
            'data':serializer.data,
            'message' : 'feedback fetched successfully'
        } , status = status.HTTP_201_CREATED)
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )


    def post(self , request , username):
        try:
            data = json.loads(request.body.decode('utf-8'))
            data['user_id'] = request.user.id
            serializer = FeedbackSerializerToPost(data = data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data':serializer.data,
                'message' : 'feedback created successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

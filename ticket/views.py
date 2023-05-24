from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import MessageSerializer
from .models import Message 
from accounts.models import User



def get_id(username):
    user = User.objects.get(username = username)
    return user.id

class MessageUnseenListView(APIView):
    def get(self , request,sender_username , receiver_username):
        try:
            if request.user.username!= sender_username and request.user.username != receiver_username:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            messages = Message.objects.filter(sender = get_id(sender_username), receiver = get_id(receiver_username), is_read = False)
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            for message in messages:
                message.is_read = True
                message.save()
            return Response({
                'data':serializer.data,
                'message' : 'messages fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class MessageGeneralListView(APIView):
    def get(self , request,sender_username , receiver_username):
        try:
            if request.user.username!= sender_username and request.user.username != receiver_username:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            messages = Message.objects.filter(sender = get_id(sender_username), receiver = get_id(receiver_username))
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            for message in messages:
                message.is_read = True
                message.save()
            return Response({
                'data':serializer.data,
                'message' : 'messages fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

    def post(self , request , sender_username):
        try:
            if request.user.username!= sender_username:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            data = request.data
            serializer = MessageSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                'data':serializer.data,
                'message' : 'messages created successfully'}
                , status = status.HTTP_201_CREATED)
            return Response({
                'data': serializer.errors,
                'message':'something went wrong'
            } , status = status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST)
        

# class MessageDetailView(APIView):
#     def get(self , request , sender_username , receiver_username):
#         message_1 = get_object_or_404(Message , sender = get_id(sender_username) , receiver = get_id(receiver_username))
#         message_2 = get_object_or_404(Message , sender = get_id(receiver_username) , receiver = get_id(sender_username) )
#         serializer_1 = MessageSerializer(message_1)
#         serializer_2 = MessageSerializer(message_2)
#         return Response(serializer_1.data , serializer_2.data)

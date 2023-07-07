from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import Message 
from accounts.models import User
from announcement.models import *
from announcement.serializers import *



def get_id(username):
    user = User.objects.get(username = username)
    return user.id

class MessageUnseenListView(APIView):
    def get(self , request,sender_username , receiver_username):
        count = 0
        try:
            if request.user.username!= sender_username and request.user.username != receiver_username:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            messages = Message.objects.filter(sender = get_id(sender_username), receiver = get_id(receiver_username), is_read = False)
            serializer = MessageSerializer(messages, many=True, context={'request': request})
            for message in messages:
                count+=1
                message.is_read = True
                message.save()
            return Response({
                'data':serializer.data,
                'count' : count,
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
        

class AllMessageDetailView(APIView):
    def get(self , request , sender_username , receiver_username):
        message_1 = Message.objects.filter(sender = get_id(sender_username) , receiver = get_id(receiver_username))
        for m in message_1:
            m.type = 'sent'
            m.save()
        message_2 = Message.objects.filter(sender = get_id(receiver_username) , receiver = get_id(sender_username) )
        for m in message_2:
            m.type = 'received'
            m.save()
        allMessage = message_1.union(message_2)
        allMessage = allMessage.order_by('created_at')
        serializer = MessageSerializer(allMessage , many=True )
        return Response(serializer.data)

class GetContacts(APIView):
    def get(self,request,username):
        user_id  = User.objects.get(username = username).id
        announcements = Announcement.objects.filter(announcer = user_id )
        volunteers = []
        for ans in announcements:
            request_announcements = AncRequest.objects.filter(req_anc = ans.id)
            for host in request_announcements:
                volunteers.append(User.objects.get(id = host.host.id))
        volunteers = list(set(volunteers))
        requests = AncRequest.objects.filter(host = user_id )
        announcers_requested = []
        for re in requests:
            ans = Announcement.objects.get(id = re.req_anc.id)
            announcers_requested.append(User.objects.get(id = ans.announcer.id))
        announcers_requested = list(set(announcers_requested))
        final_list = list(set(announcers_requested) | set(volunteers))
        serializer = ContactSerializer(final_list ,  many=True)
        return Response({
            'data':serializer.data,
            'message' : 'users fetched successfully'
        } , status = status.HTTP_201_CREATED)

class GetContactVolunteers(APIView):
    def get(self,requset , username):
        user_id  = User.objects.get(username = username).id
        announcements = Announcement.objects.filter(announcer = user_id )
        volunteers = []
        for ans in announcements:
            request_announcements = AncRequest.objects.filter(req_anc = ans.id)
            for host in request_announcements:
                volunteers.append(User.objects.get(id = host.host.id))
        volunteers = list(set(volunteers))
        serializer = ContactSerializer(volunteers ,  many=True)
        return Response({
            'data':serializer.data,
            'message' : 'users fetched successfully'
        } , status = status.HTTP_201_CREATED)

class GetContactRequest(APIView):
    def get(self,requset , username):
        user_id  = User.objects.get(username = username).id
        announcements = Announcement.objects.filter(announcer = user_id )
        requests = AncRequest.objects.filter(host = user_id )
        announcers_requested = []
        for re in requests:
            ans = Announcement.objects.get(id = re.req_anc.id)
            announcers_requested.append(User.objects.get(id = ans.announcer.id))
        announcers_requested = list(set(announcers_requested))
        serializer = ContactSerializer(announcers_requested ,  many=True)
        return Response({
            'data':serializer.data,
            'message' : 'users fetched successfully'
        } , status = status.HTTP_201_CREATED)
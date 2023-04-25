from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Blog , Tag
from announcement.models import Announcement
from .serializers import *
import json

class PublicBlogView(APIView):
    def get(self , request):
        try:
            blogs = Blog.objects.all()
            page_number = request.GET.get('page' , 1)
            paginator = Paginator(blogs , 3) #how many blogs per page
            serializer = BlogSerializer(paginator.page(page_number) , many = True)
            return Response({
                'data':serializer.data,
                'message' : 'blogs fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


class BlogView(APIView):
    permission_classes = (IsAuthenticated,)
    # Authentication_classes = []
    def get(self , request):
        try:
            blogs = Blog.objects.filter(author = request.user)
            serializer = BlogSerializer(blogs , many = True)
            return Response({
                'data':serializer.data,
                'message' : 'blogs fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


    def post(self , request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            # data = request.data
            # data._mutable = True
            data['author'] = request.user.id
            ans = Announcement.objects.get(id = data['annoncement'] )
            if ans.announcer.id != request.user.id :
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                } , status = status.HTTP_400_BAD_REQUEST)
            print("ans status = " , ans.anc_status)
            if ans.anc_status != 'D' :
                return Response({
                    'data': {},
                    'message':'the announcement status is not Done'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer = BlogSerializerToPost(data = data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data':serializer.data,
                'message' : 'blog created successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


    def patch(self , request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            # data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            if not blog.exists():
                return Response({
                    'data': {},
                    'message':'invalid blog uid'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user != blog[0].author:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            serializer = BlogSerializerToUpdate(blog[0] , data = data , partial = True)

            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'blog updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


    def delete(self , request):
        try:
            data = json.loads(request.body.decode('utf-8'))
            # data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))

            if not blog.exists():
                return Response({
                    'data': {},
                    'message':'invalid blog uid'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user != blog[0].author:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )

            blog[0].delete()
            return Response({
                'data':{},
                'message' : 'blog deleted successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class BlogDetailView(APIView):
    def get(self , request , slug):
        blog = get_object_or_404(Blog, slug=slug)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)



class TagView(APIView):
    def get(self , request):
        try:
            tags = Tag.objects.all()
            serializer = TagSerializer(tags , many = True)
            return Response({
                'data':serializer.data,
                'message' : 'tags fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class TagViewByUid(APIView):
    def get(self , request , uid):
        tag = get_object_or_404(Tag, uid=uid)
        serializer = TagSerializer(tag)
        return Response(serializer.data)
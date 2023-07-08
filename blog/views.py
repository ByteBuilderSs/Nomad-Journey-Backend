from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status , generics
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator
from .models import Blog , Tag
from like_post.models import *
from announcement.models import Announcement
from feedback.models import Feedback
from .serializers import *
from accounts.serializers import UserProfileForOverviewSerializer
import json
import random
from accounts.models import User
from rest_framework.decorators import api_view
from django.db.models import Avg, ExpressionWrapper, F , Q

@api_view(['GET'])
def GeneralBlogView(request):
    blogs = Blog.objects.all()
    serializer = GeneralBlogSerializer(blogs , many = True)
    return Response(serializer.data)     

class PublicBlogView(APIView):
    def get(self , request):
        try:
            blogs = Blog.objects.all()
            # page_number = request.GET.get('page' , 1)
            # paginator = Paginator(blogs , 3) #how many blogs per page
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
        
class MostLikedBlogView(APIView):
    def get(self , request):
        # try:
        popular_blogs = Blog.objects.annotate(num_likes=models.Count('like')).order_by('-num_likes')
        popular_blogs_images = popular_blogs.exclude(Q(main_image_64=None) | Q(main_image_64=True))
        serializer = BlogSerializer(popular_blogs_images[:5], many=True)
        return Response({
            'data':serializer.data,
            'message' : 'blogs fetched successfully'
        } , status = status.HTTP_201_CREATED)
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )

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

class AuthorLikedBlog(APIView):
    def get(self,request,username):
        user_id = User.objects.get(username = username).id
        liked_blogs = Blog.objects.filter(like__liker__username=username)
        authors = liked_blogs.values('author').distinct()
        # authors_data = []
        # for blog in liked_blogs:
        #     authors_data.append(User.objects.get(id = blog.author))
        
        authors_data = User.objects.filter(id__in=authors).order_by('id')
        serializer = UserProfileForOverviewSerializer(random.choices , many = True)
        return Response({
            'data':serializer.data,
            'message' : 'authors fetched successfully'
        } , status = status.HTTP_201_CREATED)


class BlogViewUserForView(APIView):
    def get(self , request , username):
        try:
            user_id = User.objects.get(username = username).id
            blogs = Blog.objects.filter(author = user_id)
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


    def post(self , request,username):
        # try:
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
        ans.existPost = True
        ans.save()
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
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )


    def patch(self , request, username):
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


    def delete(self , request, username):
        try:
            data = json.loads(request.body.decode('utf-8'))
            # data = request.data
            blog = Blog.objects.filter(uid = data.get('uid'))
            ans = Announcement.objects.get(id = blog[0].annoncement.id)
            # ans = Announcement.objects.get(id = data['annoncement'] )
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
            ans.existPost = False
            ans.save()
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

class SearchBlog(APIView):
    def get(self, request):
        search_query = request.query_params.get('search', '')

        queryset = Blog.objects.filter(blog_title__icontains=search_query) | \
                    Blog.objects.filter(description__icontains=search_query)

        serializer = BlogSerializer(queryset, many=True)
        return Response(serializer.data)

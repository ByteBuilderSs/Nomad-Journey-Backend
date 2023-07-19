from rest_framework import serializers
from .models import Blog , Tag
from like_post.models import Like
from feedback.models import Feedback

class GeneralBlogSerializer(serializers.ModelSerializer):
    tags_name = serializers.SerializerMethodField('get_tag_name') 
    host_firstName = serializers.SerializerMethodField('get_host_firstName')
    host_lastName = serializers.SerializerMethodField('get_host_lastName')
    host_id = serializers.SerializerMethodField('get_host_id')
    ans_city = serializers.SerializerMethodField('get_ans_city')
    trip_duration = serializers.SerializerMethodField('get_trip_duration')
    host_username = serializers.SerializerMethodField('get_host_username')
    feedback_average = serializers.SerializerMethodField('get_feedback_average')
    num_likes = serializers.SerializerMethodField('get_num_likes')
    likers = serializers.SerializerMethodField('get_likers')
    class Meta:
        model = Blog
        fields = ['uid','created_at','updated_at','author','blog_title','blog_text',
                'json_data','main_image_64','slug','tags','tags_name' ,'host_firstName','host_lastName',
                'ans_city','trip_duration' , 'host_username' , 'description' , 'secondary_image',
                'feedback_average','host_id', 'num_likes', 'likers']
    
    def get_num_likes(self, obj):
        return Like.objects.filter(liked_post = obj.uid).count
        
    def get_likers(self, obj):
        likers = []
        liker_list = Like.objects.filter(liked_post = obj.uid)
        for likes in liker_list:
            likers.append({
                "id":likes.liker.id,
                "username" : likes.liker.username,
                "first_name" : likes.liker.first_name,
                "last_name" : likes.liker.last_name
            })
        return likers


    def get_tag_name(self,obj):
        tags_name_list = []
        for t in obj.tags.all():
            tags_name_list.append(t.tag_name)
        return tags_name_list
    
    def get_host_id(self, obj):
        if obj.annoncement.main_host is not None:
            return obj.annoncement.main_host.id
        return None
    
    def get_host_firstName(self,obj):
        if obj.annoncement.main_host is not None:
            return f"{obj.annoncement.main_host.first_name}"
        return None
    
    def get_host_lastName(self,obj):
        if obj.annoncement.main_host is not None:
            return f"{obj.annoncement.main_host.last_name}"
        return None
    
    def get_ans_city(self,obj):
        return obj.annoncement.anc_city.city_name
    
    def get_trip_duration(self,obj):
        return obj.annoncement.departure_date.day - obj.annoncement.arrival_date.day
    
    def get_host_username(self,obj):
        if obj.annoncement.main_host is not None:
            return obj.annoncement.main_host.username
        return None
    
    def get_feedback_average(self, obj):
        if obj.feedback_id is not None:
            feedbacks = Feedback.objects.get(id = obj.feedback_id.id)
            return float(feedbacks.question_1 + feedbacks.question_2 + feedbacks.question_3 + feedbacks.question_4 + feedbacks.question_5)/5
        return None

class BlogSerializer(serializers.ModelSerializer):
    tags_name = serializers.SerializerMethodField('get_tag_name') 
    host_name = serializers.SerializerMethodField('get_host_name')
    author_name = serializers.SerializerMethodField('get_author_name')
    author_username = serializers.SerializerMethodField('get_author_username')
    ans_city = serializers.SerializerMethodField('get_ans_city')
    trip_duration = serializers.SerializerMethodField('get_trip_duration')
    host_username = serializers.SerializerMethodField('get_host_username')
    is_liked = serializers.SerializerMethodField('get_is_liked')
    num_likes = serializers.SerializerMethodField()
    average_rate = serializers.SerializerMethodField('get_average_rate')
    class Meta:
        model = Blog
        fields = ['uid','created_at','updated_at','author','blog_title','blog_text',
                'json_data','main_image_64','slug','tags','tags_name' ,'host_name',
                'ans_city','trip_duration' , 'host_username' , 'description' , 'secondary_image',
                'is_liked', 'num_likes' , 'average_rate'  , 'author_name' , 'author_username']
    
    def get_tag_name(self,obj):
        tags_name_list = []
        for t in obj.tags.all():
            tags_name_list.append(t.tag_name)
        return tags_name_list
    
    def get_host_name(self,obj):
        if obj.annoncement.main_host is not None:
            return f"{obj.annoncement.main_host.first_name} {obj.annoncement.main_host.last_name}"
        return None
    
    def get_ans_city(self,obj):
        return obj.annoncement.anc_city.city_name
    
    def get_trip_duration(self,obj):
        return obj.annoncement.departure_date.day - obj.annoncement.arrival_date.day
    
    def get_host_username(self,obj):
        if obj.annoncement.main_host is not None:
            return obj.annoncement.main_host.username
        return None
    def get_average_rate(self,obj):
        if obj.feedback_id is not None:
            return float(obj.feedback_id.question_1 + obj.feedback_id.question_2 + obj.feedback_id.question_3 + obj.feedback_id.question_4 + obj.feedback_id.question_5)/5
        else:
            return 0
    def get_is_liked(self,obj):
        like = Like.objects.filter(liked_post = obj.uid)
        likers = []
        if like is not None:
            for liker in like:
                likers.append(liker.liker.id)
            return likers
        return None
    
    def get_num_likes(self, obj):
        like = Like.objects.filter(liked_post = obj.uid)
        likers = []
        if like is not None:
            for liker in like:
                likers.append(liker.liker.id)
        return len(likers)

    def get_author_name(self,obj):
        return f"{obj.author.first_name} {obj.author.last_name}"
    
    def get_author_username(self,obj):
        return obj.author.username

class BlogSerializerToPost(serializers.ModelSerializer):
    tags_name = serializers.SerializerMethodField('get_tag_name') 
    class Meta:
        model = Blog
        fields = ['uid','created_at','updated_at','author','blog_title','blog_text','json_data','main_image_64','slug','tags','tags_name',
                'annoncement', 'description' , 'secondary_image']
    
    def get_tag_name(self,obj):
        tags_name_list = []
        for t in obj.tags.all():
            tags_name_list.append(t.tag_name)
        return tags_name_list
    

class BlogSerializerToUpdate(serializers.ModelSerializer):
    tags_name = serializers.SerializerMethodField('get_tag_name') 
    class Meta:
        model = Blog
        fields = ['uid','created_at','updated_at','author','blog_title','blog_text',
                'json_data','main_image_64','slug','tags','tags_name' , 'description' , 'secondary_image']
    
    def get_tag_name(self,obj):
        tags_name_list = []
        for t in obj.tags.all():
            tags_name_list.append(t.tag_name)
        return tags_name_list


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("__all__")
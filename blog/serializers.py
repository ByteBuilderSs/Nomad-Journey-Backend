from rest_framework import serializers
from .models import Blog , Tag

class BlogSerializer(serializers.ModelSerializer):
    tags_name = serializers.SerializerMethodField('get_tag_name') 
    host_name = serializers.SerializerMethodField('get_host_name')
    ans_city = serializers.SerializerMethodField('get_ans_city')
    trip_duration = serializers.SerializerMethodField('get_trip_duration')
    host_username = serializers.SerializerMethodField('get_host_username')
    class Meta:
        model = Blog
        fields = ['uid','created_at','updated_at','author','blog_title','blog_text',
                'json_data','main_image_64','slug','tags','tags_name' ,'host_name',
                'ans_city','trip_duration' , 'host_username' , 'description' , 'secondary_image']
    
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
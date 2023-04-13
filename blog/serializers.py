from rest_framework import serializers
from .models import Blog , Tag

class BlogSerializer(serializers.ModelSerializer):
    tags_name = serializers.SerializerMethodField('get_tag_name') 
    class Meta:
        model = Blog
        fields = ['uid','created_at','updated_at','author','blog_title','blog_text','json_data','main_image_64','slug','tags','tags_name']
    
    def get_tag_name(self,obj):
        tags_name_list = []
        for t in obj.tags.all():
            tags_name_list.append(t.tag_name)
        return tags_name_list



class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("__all__")
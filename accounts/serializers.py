from rest_framework import serializers
from .models import User , Language , UserInterest
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from NormandJourney.tools import hash_sha256
from datetime import date
from announcement.models import Announcement
from blog.models import Blog

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_again', 'username' , 'User_city']
        extra_kwargs = {
            'password':{'write_only' : True},
            'password_again':{'write_only' : True}
        }
    
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        instance.password_again = hash_sha256(instance.password_again)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserCompeleteProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("__all__")
        extra_kwargs = {
            'password':{'write_only' : True},
            'password_again':{'write_only' : True}
        }

class UserProfileEdit1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','User_birthdate','User_gender','User_phone_number']


class UserProfileEdit2Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['User_address','User_apt','User_city','User_country','User_postal_code']

class GetUsernameAndUserImageByUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','profile_photo' , 'image_code']

class UserProfileEdit3Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['hosting_availability','hometown','User_job','User_education','User_about_me','why_Im_on_nomadjourney',
                'favorite_music_movie_book','amazing_thing_done','teach_learn_share','what_Ican_share_with_host','interests',
                'langF','langL']
        
class UserProfileEdit4Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image_code']

class UserProfileForOverviewSerializer(serializers.ModelSerializer):
    user_age = serializers.SerializerMethodField('get_user_age')
    joined_since = serializers.SerializerMethodField('get_joined_since')
    posts_count = serializers.SerializerMethodField('get_post_count')
    announcements_count = serializers.SerializerMethodField('get_announcement_count')

    class Meta:
        model = User
        fields = ['announcements_count','user_age','User_gender','User_job','joined_since', 'posts_count','User_city','User_education']
    
    def get_user_age(self,obj):
        try:
            today = date.today()
            age = today.year - obj.User_birthdate.year - ((today.month, today.day) < (obj.User_birthdate.month, obj.User_birthdate.day))
            return age
        except:
            return 0
    
    def get_joined_since(self,obj):
        today = date.today()
        joined_since = today.day - obj.date_joined.day
        return joined_since
    
    def get_post_count(self , obj):
        return Blog.objects.filter(author = obj.id).count()
    
    def get_announcement_count(self , obj):
        return Announcement.objects.filter(announcer = obj.id).count()

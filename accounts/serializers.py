from rest_framework import serializers
from .models import User , Language , UserInterest
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from NormandJourney.tools import hash_sha256
from datetime import datetime
from announcement.models import Announcement
from blog.models import Blog


class UserSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField('get_city_name') 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_again', 'username' , 'User_city' , 'city_name']
        extra_kwargs = {
            'password':{'write_only' : True},
            'password_again':{'write_only' : True}
        }
    def get_city_name(self,obj):
        return obj.User_city.city_name
    def create(self, validated_data):
        password = validated_data.pop('password',None)
        instance = self.Meta.model(**validated_data)
        instance.password_again = hash_sha256(instance.password_again)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

class UserCompeleteProfileSerializer(serializers.ModelSerializer):
    intrest_name = serializers.SerializerMethodField('get_intrest_name') 
    langL_name = serializers.SerializerMethodField('get_langL_name') 
    langF_name = serializers.SerializerMethodField('get_langF_name') 
    city_name = serializers.SerializerMethodField('get_city_name') 
    city_country = serializers.SerializerMethodField('get_city_country')
    class Meta:
        model = User
        fields = ['User_birthdate','User_about_me','User_job','User_education','password',
                'User_nationality','User_address','User_address_lat','User_address_long','User_gender','User_country_code',
                'User_city','User_apt','User_postal_code','User_phone_number','image_code','profile_photo','ssn','first_name','last_name',
                'email','username','date_joined','hosting_availability','hometown','why_Im_on_nomadjourney','favorite_music_movie_book',
                'amazing_thing_done','teach_learn_share','what_Ican_share_with_host','interests','langF','langL', 'city_name', 'city_country', 'intrest_name',
                'langL_name' , 'langF_name']
        extra_kwargs = {
            'password':{'write_only' : True},
            'password_again':{'write_only' : True}
        }
    def get_intrest_name(self,obj):
        intrest_name_list = []
        for i in obj.interests.all():
            intrest_name_list.append(i.interest_name)
        return intrest_name_list

    def get_langL_name(self,obj):
        langL_name_list = []
        for t in obj.langL.all():
            langL_name_list.append(t.language_name)
        return langL_name_list

    def get_langF_name(self,obj):
        langF_name_list = []
        for t in obj.langF.all():
            langF_name_list.append(t.language_name)
        return langF_name_list

    def get_city_name(self,obj):
        return obj.User_city.city_name

    def get_city_country(self,obj):
        return obj.User_city.country

class UserProfileEdit1Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name','last_name','username','User_birthdate','User_gender','User_phone_number']


class UserProfileEdit2Serializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField('get_city_name') 
    city_country = serializers.SerializerMethodField('get_city_country') 

    class Meta:
        model = User
        fields = ['User_address','User_apt','User_city','User_postal_code' , 'city_name', 'city_country']
    def get_city_name(self,obj):
        return obj.User_city.city_name
    
    def get_city_country(self, obj):
        return obj.User_city.country

class GetUsernameAndUserImageByUserIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','profile_photo' , 'image_code']

class UserProfileEdit3Serializer(serializers.ModelSerializer):
    interests = serializers.SlugRelatedField(
        slug_field="interest_name",
        queryset=UserInterest.objects.all(),
        many=True)
    intrest_name = serializers.SerializerMethodField('get_intrest_name') 
    langL_name = serializers.SerializerMethodField('get_langL_name') 
    langF_name = serializers.SerializerMethodField('get_langF_name') 
    class Meta:
        model = User
        fields = ['hosting_availability','hometown','User_job','User_education','User_about_me','why_Im_on_nomadjourney',
                'favorite_music_movie_book','amazing_thing_done','teach_learn_share','what_Ican_share_with_host','interests',
                'langF','langL','intrest_name','langL_name','langF_name']

    def get_intrest_name(self,obj):
        intrest_name_list = []
        for i in obj.interests.all():
            intrest_name_list.append(i.interest_name)
        return intrest_name_list

    def get_langL_name(self,obj):
        langL_name_list = []
        for t in obj.langL.all():
            langL_name_list.append(t.language_name)
        return langL_name_list

    def get_langF_name(self,obj):
        langF_name_list = []
        for t in obj.langF.all():
            langF_name_list.append(t.language_name)
        return langF_name_list

class UserProfileEdit4Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['image_code']

class UserProfileForOverviewSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField('get_city_name') 
    user_age = serializers.SerializerMethodField('get_user_age')
    joined_since = serializers.SerializerMethodField('get_joined_since')
    posts_count = serializers.SerializerMethodField('get_post_count')
    announcements_count = serializers.SerializerMethodField('get_announcement_count')
    intrest_name = serializers.SerializerMethodField('get_intrest_name') 
    langL_name = serializers.SerializerMethodField('get_langL_name') 
    langF_name = serializers.SerializerMethodField('get_langF_name') 

    class Meta:
        model = User
        fields = ['user_age','joined_since','posts_count','announcements_count','User_birthdate','User_about_me','User_job','User_education',
                'User_nationality','User_address','User_address_lat','User_address_long','User_gender','User_country_code',
                'User_city','User_apt','User_postal_code','User_phone_number','image_code','profile_photo','ssn','first_name','last_name',
                'email','username','date_joined','hosting_availability','hometown','why_Im_on_nomadjourney','favorite_music_movie_book',
                'amazing_thing_done','teach_learn_share','what_Ican_share_with_host','interests','langF','langL' , 'city_name' , 'intrest_name',
                'langL_name' , 'langF_name']
    def get_city_name(self,obj):
        return obj.User_city.city_name
    def get_user_age(self,obj):
        try:
            today = datetime.today()
            age = today.year - obj.User_birthdate.year - ((today.month, today.day) < (obj.User_birthdate.month, obj.User_birthdate.day))
            return age
        except:
            return 0
    
    def get_joined_since(self,obj):
        today = datetime.today()
        joined_since = abs(today.day - obj.date_joined.day)
        if joined_since == 0:
            joined_since = abs(today.hour - obj.date_joined.hour)
            if joined_since == 0:
                joined_since = abs(today.minute - obj.date_joined.minute)
                if joined_since == 0:
                    joined_since = abs(today.second - obj.date_joined.second)
                    return f"{joined_since} seconds"
                else:
                    return f"{joined_since} minutes"
            else:
                return f"{joined_since} hours"
        else:
            return f"{joined_since} days"


    def get_post_count(self , obj):
        return Blog.objects.filter(author = obj.id).count()
    
    def get_announcement_count(self , obj):
        return Announcement.objects.filter(announcer = obj.id).count()

    def get_intrest_name(self,obj):
        intrest_name_list = []
        for i in obj.interests.all():
            intrest_name_list.append(i.interest_name)
        return intrest_name_list

    def get_langL_name(self,obj):
        langL_name_list = []
        for t in obj.langL.all():
            langL_name_list.append(t.language_name)
        return langL_name_list

    def get_langF_name(self,obj):
        langF_name_list = []
        for t in obj.langF.all():
            langF_name_list.append(t.language_name)
        return langF_name_list

class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = ("__all__")
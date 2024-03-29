from rest_framework import serializers
from .models import User , Language , UserInterest
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from NormandJourney.tools import hash_sha256
from datetime import datetime
from announcement.models import Announcement
from blog.models import Blog
from utils.models import *


class UserSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField('get_city_name') 
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_again', 'username' , 'User_city' , 'city_name' , 'coins' , 'reset_token',
                'reset_token_expiry']
        extra_kwargs = {
            'password':{'write_only' : True},
            'password_again':{'write_only' : True},
            'coins' : {'read_only' : True}
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
    city_lat = serializers.SerializerMethodField()
    city_long = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'User_birthdate','User_about_me','User_job','User_education','password',
                'User_nationality','User_address','User_address_lat','User_address_long','User_gender','User_country_code',
                'User_city','User_apt','User_postal_code','User_phone_number', 'ssn','first_name','last_name',
                'email','username','date_joined','hosting_availability','hometown','why_Im_on_nomadjourney','favorite_music_movie_book',
                'amazing_thing_done','teach_learn_share','what_Ican_share_with_host','interests','langF','langL', 'city_name', 'city_country', 'intrest_name',
                'langL_name' , 'langF_name' , 'coins','User_address_lat','User_address_long','city_lat','city_long']
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

    def get_city_lat(self, obj):
        city = City.objects.get(id = obj.User_city.id)
        return city.c_lat
    
    def get_city_long(self, obj):
        city = City.objects.get(id = obj.User_city.id)
        return city.c_long

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

# class GetUsernameAndUserImageByUserIdSerializer(serializers.ModelSerializer):
#     profile_photo_base64 = serializers.SerializerMethodField()

#     class Meta:
#         model = User
#         fields = ['username', 'profile_photo_base64']

#     def get_profile_photo_base64(self, obj):
#         if obj.profile_photo:
#             with open(obj.profile_photo.path, "rb") as image_file:
#                 encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
#                 return encoded_string
#         else:
#             return None

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
        fields = ['profile_photo']

    def update(self, instance, validated_data):
        print(instance)
        print(validated_data)
        print(validated_data['profile_photo'] is None)
        if validated_data['profile_photo'] is None:
            validated_data['profile_photo'] = ""
        # instance.profile_photo = validated_data.get('profile_photo', instance.profile_photo)
        # print(validated_data)
        # instance.save()
        # return instance
        return super().update(instance, validated_data)

class UserProfileEdit5Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_sun','is_sat','is_mon','is_tue','is_wed','is_thu','is_fri','maximum_number_of_guests',
                'prefered_gender_to_host','is_pet_friendly','is_kid_friendly','is_smoking_allowed','sleeping_arrangments',
                'description_of_sleeping_arrangement','roommate_situation','additional_information','i_have_pet','kids_at_home',
                'smoking_at_home','wheelchair_accessible' , 'User_address_lat' , 'User_address_long']


class UserProfileEdit6Serializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField('get_city_name') 
    city_country = serializers.SerializerMethodField('get_city_country') 

    class Meta:
        model = User
        fields = ['User_address','User_apt','User_city','User_postal_code' , 'city_name',
                'city_country' , 'User_address_lat' , 'User_address_long']
    def get_city_name(self,obj):
        return obj.User_city.city_name
    
    def get_city_country(self, obj):
        return obj.User_city.country
    
class UserProfileEdit7Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['sleeping_arrangments','description_of_sleeping_arrangement',
                'roommate_situation','additional_information','i_have_pet','kids_at_home',
                'smoking_at_home','wheelchair_accessible']

class UserProfileEdit8Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['is_sun','is_sat','is_mon','is_tue','is_wed','is_thu','is_fri','maximum_number_of_guests',
                'prefered_gender_to_host','is_pet_friendly','is_kid_friendly','is_smoking_allowed']

class UserProfileEdit9Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['old_password' , 'new_password']
        extra_kwargs = {
            'old_password':{'write_only' : True},
            'new_password':{'write_only' : True}
        }

class UserProfileEdit10Serializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password' , 'new_email']
        extra_kwargs = {
            'password':{'write_only' : True}
        }


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
                'User_city','User_apt','User_postal_code','User_phone_number', 'ssn','first_name','last_name',
                'email','username','date_joined','hosting_availability','hometown','why_Im_on_nomadjourney','favorite_music_movie_book',
                'amazing_thing_done','teach_learn_share','what_Ican_share_with_host','interests','langF','langL' , 'city_name' , 'intrest_name',
                'langL_name' , 'langF_name' , 'id' , 'coins']
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
        now = datetime.now(obj.date_joined.tzinfo)
        joined_time = obj.date_joined.astimezone(None)
        delta = now - joined_time

        days = delta.days
        seconds = delta.seconds
        hours, remainder = divmod(seconds, 3600)
        minutes, seconds = divmod(remainder, 60)

        if days > 0:
            return f"{days} day{'s' if days > 1 else ''}, {hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}, {seconds} second{'s' if seconds > 1 else ''}"
        elif hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}, {seconds} second{'s' if seconds > 1 else ''}"
        elif minutes > 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''}, {seconds} second{'s' if seconds > 1 else ''}"
        else:
            return f"{seconds} second{'s' if seconds > 1 else ''}"


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

class UserProfilePhotoSerializer(serializers.ModelSerializer):
    profile_photo_URL = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['profile_photo', 'profile_photo_URL']

    def get_profile_photo_URL(self, obj):
        if obj.profile_photo:
            return obj.profile_photo.url
        return None
    
class UserAddCoinSerializerGet(serializers.ModelSerializer):
    price = serializers.SerializerMethodField('get_price') 
    class Meta:
        model = User
        fields = ['coins' , 'coin_to_buy' , 'price']
    def get_price(self,obj):
        return obj.coin_to_buy * 25000

class UserAddCoinSerializerPut(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['coin_to_buy']
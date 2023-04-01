from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login
from rest_framework import serializers
from NormandJourney.tools import hash_sha256

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password', 'password_again', 'username']
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

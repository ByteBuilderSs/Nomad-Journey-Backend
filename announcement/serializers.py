from rest_framework import serializers
from .models import Announcement
from accounts.models import User


class AnnouncementSerializer(serializers.ModelSerializer):
    # city_name = serializers.SerializerMethodField()
    # city_country = serializers.SerializerMethodField() 
    announcer_username = serializers.SerializerMethodField() 
    announcer_image_code = serializers.SerializerMethodField() 
    announcer_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Announcement
        fields = ['id','announcer', 'anc_city', 'anc_country', 'anc_status', 'arrival_date', 'departure_date', 'arrival_date_is_flexible',
                   'departure_date_is_flexible', 'anc_description', 'travelers_count', 'announcer_username', 'announcer_image_code', 'announcer_name']

    def create(self, validated_data):
        validated_data['announcer'] = self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    # def get_city_name(self, obj):
    #     city = City.objects.get(id = obj.anc_city.id)
    #     return city.city_name
    
    # def get_city_country(self, obj):
    #     city = City.objects.get(id = obj.anc_city.id)
    #     return city.country
    
    def get_announcer_username(self, obj):
        user = User.objects.get(id = obj.announcer.id)
        return user.username
    
    def get_announcer_image_code(self, obj):
        user = User.objects.get(id = obj.announcer.id)
        return user.image_code
    
    def get_announcer_name(self, obj):
        user = User.objects.get(id=obj.announcer.id)
        return user.first_name + ' ' + user.last_name


class UnAuthAnnouncementDetailsSerializer(serializers.ModelSerializer):
    # city_name = serializers.SerializerMethodField()
    # city_country = serializers.SerializerMethodField()
    # city_lat = serializers.SerializerMethodField()
    # city_long = serializers.SerializerMethodField()
    host_firstName = serializers.SerializerMethodField()
    host_lastName = serializers.SerializerMethodField()
    host_username = serializers.SerializerMethodField()
    host_nationality = serializers.SerializerMethodField()
    host_birthdate = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id', 'announcer', 'anc_city', 'anc_country', 'anc_status', 'arrival_date', 'departure_date', 'arrival_date_is_flexible',
                    'departure_date_is_flexible', 'anc_description', 'travelers_count',
                    'host_firstName', 'host_lastName', 'host_username', 'host_nationality', 'host_birthdate']

    # def get_city_name(self, obj):
    #     city = City.objects.get(id = obj.anc_city.id)
    #     return city.city_name
    
    # def get_city_country(self, obj):
    #     city = City.objects.get(id = obj.anc_city.id)
    #     return city.country
    
    # def get_city_lat(self, obj):
    #     city = City.objects.get(id = obj.anc_city.id)
    #     return city.c_lat
    
    # def get_city_long(self, obj):
    #     city = City.objects.get(id = obj.anc_city.id)
        # return city.c_long
    
    def get_host_firstName(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.first_name
        return host

    def get_host_lastName(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.last_name
        return host
    
    def get_host_username(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.username
        return host
    
    def get_host_nationality(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.User_nationality
        return host
    
    def get_host_birthdate(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.User_birthdate
        return host

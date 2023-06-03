from rest_framework import serializers
from .models import Announcement
from accounts.models import User
from accounts.serializers import UserSerializer
from anc_request.models import AncRequest
from utils.models import City
import datetime


class AnnouncementSerializer(serializers.ModelSerializer):
    announcer_username = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    city_country = serializers.SerializerMethodField()
    anc_status = serializers.SerializerMethodField()
    announcer_langs = serializers.SerializerMethodField()
    announcer_profile_photo = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id','announcer', 'anc_city', 'city_name', 'city_country', 'anc_status', 'arrival_date', 'departure_date', 'stay_duration', 'arrival_date_is_flexible',
                    'departure_date_is_flexible', 'anc_description', 'travelers_count', 'announcer_username', 'anc_timestamp_created', 'announcer_langs', 'announcer_profile_photo']

    def create(self, validated_data):
        validated_data['announcer'] = self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_anc_status(self, obj):
        current_time = datetime.datetime.now().date()
        if obj.anc_status == 'P' and current_time >= obj.arrival_date:
            return 'E'
        elif obj.anc_status == 'A' and current_time >= obj.departure_date:
            return 'D'
        else:
            return obj.anc_status

    def get_city_name(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.city_name

    def get_city_country(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.country

    def get_announcer_username(self, obj):
        user = User.objects.get(id = obj.announcer.id)
        return user.username

    def get_announcer_langs(self, obj):
        user = User.objects.get(id = obj.announcer.id)
        return list(user.langF.values_list('id', flat=True)) + list(user.langL.values_list('id', flat=True))
    
    def get_announcer_profile_photo(self, obj):
        user = User.objects.get(id=obj.announcer.id)
        try:
            return user.profile_photo
        except:
            return None

class FuckingAnnouncementSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    city_country = serializers.SerializerMethodField() 
    announcer_username = serializers.SerializerMethodField() 
    main_host_name = serializers.SerializerMethodField()
    main_host_username = serializers.SerializerMethodField()
    hosts = serializers.SerializerMethodField()
    anc_status = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id','announcer', 'anc_city', 'city_name', 'city_country', 'anc_status', 'arrival_date', 'departure_date', 'stay_duration', 'arrival_date_is_flexible',
                    'departure_date_is_flexible', 'anc_description', 'travelers_count', 'anc_timestamp_created', 'announcer_username', 'main_host_name', 'main_host_username', 'hosts']

    def create(self, validated_data):
        validated_data['announcer'] = self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

    def get_anc_status(self, obj):
        current_time = datetime.datetime.now().date()
        if obj.anc_status == 'P' and current_time > obj.arrival_date:
            return 'E'
        elif obj.anc_status == 'A' and current_time > obj.departure_date:
            return 'D'
        else:
            return obj.anc_status

    def get_city_name(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.city_name
    
    def get_city_country(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.country
    
    def get_announcer_username(self, obj):
        user = User.objects.get(id = obj.announcer.id)
        return user.username

    def get_main_host_name(self, obj):
        main_host = obj.main_host
        if main_host is not None:
            user = User.objects.get(id=main_host.id)
            return user.first_name + ' ' + user.last_name
        return main_host
    
    def get_main_host_username(self, obj):
        main_host = obj.main_host
        if main_host is not None:
            user = User.objects.get(id=main_host.id)
            return user.username
        return main_host

    def get_hosts(self, obj):
        hosts = obj.hosts
        if hosts is not None:
            serializer = UserSerializer(hosts, many=True)
            return serializer.data
        return hosts


class UnAuthAnnouncementDetailsSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    city_country = serializers.SerializerMethodField()
    city_lat = serializers.SerializerMethodField()
    city_long = serializers.SerializerMethodField()
    host_id = serializers.SerializerMethodField()
    host_firstName = serializers.SerializerMethodField()
    host_lastName = serializers.SerializerMethodField()
    host_username = serializers.SerializerMethodField()
    host_nationality = serializers.SerializerMethodField()
    host_birthdate = serializers.SerializerMethodField()
    host_latitude = serializers.SerializerMethodField()
    host_longitude = serializers.SerializerMethodField()
    announcer_firstName = serializers.SerializerMethodField()
    announcer_lastName = serializers.SerializerMethodField()
    announcer_username = serializers.SerializerMethodField()
    announcer_nationality = serializers.SerializerMethodField()
    announcer_birthdate = serializers.SerializerMethodField()
    volunteers = serializers.SerializerMethodField()
    anc_status = serializers.SerializerMethodField()

    class Meta:
        model = Announcement
        fields = ['id', 'announcer', 'anc_city', 'city_name', 'city_country', 'city_lat', 'city_long', 'anc_status', 'arrival_date', 'departure_date', 'stay_duration', 'arrival_date_is_flexible',
                    'departure_date_is_flexible', 'anc_description', 'travelers_count', 'anc_timestamp_created',
                    'host_id', 'host_firstName', 'host_lastName', 'host_username', 'host_nationality', 'host_birthdate', 'host_latitude', 'host_longitude',
                    'announcer_firstName', 'announcer_lastName', 'announcer_username', 'announcer_nationality', 'announcer_birthdate', 'volunteers']

    def get_anc_status(self, obj):
        current_time = datetime.datetime.now().date()
        if obj.anc_status == 'P' and current_time > obj.arrival_date:
            return 'E'
        elif obj.anc_status == 'A' and current_time > obj.departure_date:
            return 'D'
        else:
            return obj.anc_status

    def get_city_name(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.city_name
    
    def get_city_country(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.country
    
    def get_city_lat(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.c_lat
    
    def get_city_long(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.c_long
    
    def get_announcer_firstName(self, obj):
        announcer = User.objects.get(id = obj.announcer.id)
        return announcer.first_name

    def get_announcer_lastName(self, obj):
        announcer = User.objects.get(id = obj.announcer.id)
        return announcer.last_name
    
    def get_announcer_username(self, obj):
        announcer = User.objects.get(id = obj.announcer.id)
        return announcer.username
    
    def get_announcer_nationality(self, obj):
        announcer = User.objects.get(id = obj.announcer.id)
        return announcer.User_nationality
    
    def get_announcer_birthdate(self, obj):
        announcer = User.objects.get(id = obj.announcer.id)
        return announcer.User_birthdate


    def get_host_id(self, obj):
        host = obj.main_host
        if host is not None:
            return host.id
        return host

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
    
    def get_host_longitude(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.User_address_long
        return host

    def get_host_latitude(self, obj):
        host = obj.main_host
        if host is not None:
            host = User.objects.get(id = host.id)
            return host.User_address_lat
        return host
    
    def get_volunteers(self, obj):
        hosts = []
        request_announcements = AncRequest.objects.filter(req_anc = obj.id)
        for host in request_announcements:
            hosts.append({
                "id":host.host.id,
                "username" : host.host.username,
                "first_name" : host.host.first_name,
                "last_name" : host.host.last_name,
                "host_lat": host.host.User_address_lat,
                "host_long": host.host.User_address_long
            })
        return hosts



class DoneStatusAnnouncementsSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    city_country = serializers.SerializerMethodField()
    main_host_name = serializers.SerializerMethodField()
    main_host_username = serializers.SerializerMethodField()
    class Meta:
        model = Announcement
        fields = ['city_name', 'city_country', 'main_host_name', 'main_host_username']

    def get_city_name(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.city_name
    
    def get_city_country(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.country
    
    def get_main_host_name(self, obj):
        main_host = obj.main_host
        if main_host is not None:
            user = User.objects.get(id=main_host.id)
            return user.first_name + ' ' + user.last_name
        return main_host
    
    def get_main_host_username(self, obj):
        main_host = obj.main_host
        if main_host is not None:
            user = User.objects.get(id=main_host.id)
            return user.username
        return main_host
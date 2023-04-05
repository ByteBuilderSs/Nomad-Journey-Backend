from rest_framework import serializers
from .models import Announcement
from accounts.models import User


class AnnouncementSerializer(serializers.ModelSerializer):
    # city_name = serializers.SerializerMethodField()
    # city_country = serializers.SerializerMethodField() 
    announcer_username = serializers.SerializerMethodField() 
    announcer_image_code = serializers.SerializerMethodField() 
    
    class Meta:
        model = Announcement
        fields = ['id','announcer', 'anc_city', 'anc_country', 'anc_status', 'arrival_date', 'departure_date', 'arrival_date_is_flexible',
                   'departure_date_is_flexible', 'anc_description', 'travelers_count', 'announcer_username', 'announcer_image_code']

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
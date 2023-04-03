from rest_framework import serializers
from .models import Announcement
from accounts.models import City


class AnnouncementSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    city_country = serializers.SerializerMethodField() 
    class Meta:
        model = Announcement
        fields = ['id','announcer', 'anc_city', 'anc_status', 'arrival_date', 'departure_date', 'arrival_date_is_flexible',
                   'departure_date_is_flexible', 'anc_description', 'travelers_count', 'city_name', 'city_country']

    def create(self, validated_data):
        validated_data['announcer'] = self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
    
    def get_city_name(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.city_name
    
    def get_city_country(self, obj):
        city = City.objects.get(id = obj.anc_city.id)
        return city.country
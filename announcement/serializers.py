from rest_framework import serializers
from .models import Announcement


class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['announcer', 'anc_city', 'anc_country', 'arrival_date', 'departure_date', 'arrival_date_is_flexible',
                   'departure_date_is_flexible', 'anc_description', 'travelers_count']

    def create(self, validated_data):
        validated_data['announcer'] = self.context['request'].user
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
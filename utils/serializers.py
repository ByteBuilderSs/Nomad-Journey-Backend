from rest_framework import serializers
from .models import City


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'country']


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'
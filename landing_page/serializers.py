from rest_framework import serializers
from utils.models import City

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('city_name', 'country', 'c_lat', 'c_long', 'city_image64', 'abbrev_city' , 'area' , 'population',
                    'currency','explore_more')

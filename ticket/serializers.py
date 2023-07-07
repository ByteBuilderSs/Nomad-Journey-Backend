from rest_framework import serializers
from .models import Message
from accounts.models import User
from utils.models import City
from announcement.models import Announcement
class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'created_at' , 'is_read','ans_id' , 'type']
        extra_kwargs = {
            'type' : {'read_only' : True}
        }


class ContactRequestSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    anc_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id', 'username' , 'city_name' , 'anc_id']

    def get_city_name(self, obj):
        city = City.objects.get(id = obj.User_city.id)
        return city.city_name
    
    def get_anc_id(self,obj):
        anc_id = Announcement.objects.get(host = obj.id).id
        return anc_id
    
class ContactVolunteerSerializer(serializers.ModelSerializer):
    city_name = serializers.SerializerMethodField()
    anc_id = serializers.SerializerMethodField()
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id', 'username' , 'city_name' , 'anc_id']

    def get_city_name(self, obj):
        city = City.objects.get(id = obj.User_city.id)
        return city.city_name
    
    def get_anc_id(self,obj):
        anc_id = Announcement.objects.get(announcer = obj.id).id
        return anc_id
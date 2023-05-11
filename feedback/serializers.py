from rest_framework import serializers
from .models import Feedback
from accounts.models import User

class FeedbackSerializerToGet(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField('get_average_rate') 
    username = serializers.SerializerMethodField('get_username') 
    host_name = serializers.SerializerMethodField('get_host_name')
    ans_city = serializers.SerializerMethodField('get_ans_city')
    trip_duration = serializers.SerializerMethodField('get_trip_duration')
    host_username = serializers.SerializerMethodField('get_host_username')
    class Meta:
        model = Feedback
        fields = ['username','question_1','question_2','question_3','question_4','question_5','average_rate' , 'host_name' , 'ans_city',
                'trip_duration' , 'host_username']

    def get_average_rate(self,obj):
        return float(obj.question_1 + obj.question_2 + obj.question_3 + obj.question_4 + obj.question_5)/5
    def get_username(self,obj):
        return User.objects.get(id = obj.user_id.id).username
    def get_host_name(self,obj):
        if obj.ans_id.main_host is not None:
            return f"{obj.ans_id.main_host.first_name} {obj.ans_id.main_host.last_name}"
        return None
    def get_ans_city(self,obj):
        return obj.ans_id.anc_city.city_name
    
    def get_trip_duration(self,obj):
        return obj.ans_id.departure_date.day - obj.ans_id.arrival_date.day
    
    def get_host_username(self,obj):
        if obj.ans_id.main_host is not None:
            return obj.ans_id.main_host.username
        return None
class FeedbackSerializerToPost(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user_id','question_1','question_2','question_3','question_4','question_5' , 'ans_id']

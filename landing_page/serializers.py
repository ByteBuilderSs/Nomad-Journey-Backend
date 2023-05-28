from rest_framework import serializers
from django.db.models import Avg, ExpressionWrapper, F , Q
from utils.models import City
from announcement.models import Announcement
from feedback.models import *

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ('city_name', 'country', 'c_lat', 'c_long', 'city_small_image64','city_big_image64', 'abbrev_city' , 'area' , 'population',
                    'currency','explore_more')
        

class MostRatedHostSerializer(serializers.ModelSerializer):
    announcer_username = serializers.SerializerMethodField('get_announcer_username') 
    anc_city = serializers.SerializerMethodField('get_anc_city') 
    city_image = serializers.SerializerMethodField('get_city_image') 
    avg_feedback = serializers.SerializerMethodField('get_avg_feedback') 
    profile_photo = serializers.SerializerMethodField('get_profile_phot') 

    class Meta:
        Model = Announcement
        fields = ('id','announcer_username' , 'announcer' ,'anc_city', 'arrival_date','departure_date','travelers_count' , 'profile_photo')
    
    def get_announcer_username(obj,self):
        return obj.announcer.username,

    def get_anc_city(obj,self):
        return obj.anc_city.city_name

    def get_city_image(obj,self):
        obj.anc_city.city_small_image64

    def get_avg_feedback(obj,self):
        avg_feedbacks = Feedback.objects.values('ans_id__main_host').annotate(
        avg_feedback=Avg(F('question_1') + F('question_2') + F('question_3') + F('question_4') + F('question_5')) / 5)
        max_avg_feedback = avg_feedbacks.order_by('-avg_feedback').first()
        max_avg_feedback_value = max_avg_feedback['avg_feedback']
        announcements = Announcement.objects.filter(main_host=max_avg_feedback['ans_id__main_host'])
        avg_feedback = Feedback.objects.filter(ans_id=obj.id).aggregate(
            avg_feedback=Avg(F('question_1') + F('question_2') + F('question_3') + F('question_4') + F('question_5')) / 5
        )
        return avg_feedback['avg_feedback']
    
    def get_profile_phot(self,obj):
        return obj.announcer.profile_photo

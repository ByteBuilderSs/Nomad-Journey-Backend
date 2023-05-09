from rest_framework import serializers
from .models import Feedback

class FeedbackSerializerToGet(serializers.ModelSerializer):
    average_rate = serializers.SerializerMethodField('get_average_rate') 
    class Meta:
        model = Feedback
        fields = ['question_1','question_2','question_3','question_4','question_5','average_rate']

    def get_average_rate(self,obj):
        return float(obj.question_1 + obj.question_2 + obj.question_3 + obj.question_4 + obj.question_5)/5

class FeedbackSerializerToPost(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['question_1','question_2','question_3','question_4','question_5']

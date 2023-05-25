from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'created_at' , 'is_read','ans_id' , 'type']
        extra_kwargs = {
            'type' : {'read_only' : True}
        }
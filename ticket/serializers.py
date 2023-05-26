from rest_framework import serializers
from .models import Message

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'created_at' , 'is_read','ans_id' , 'type']
        extra_kwargs = {
            'type' : {'read_only' : True}
        }

class MessageUnseenSerializer(serializers.ModelSerializer):
    unseen_messages_count = serializers.SerializerMethodField('get_unseen_messages_count') 
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'created_at' , 'is_read','ans_id' , 'type','unseen_messages_count']
        extra_kwargs = {
            'type' : {'read_only' : True}
        }
    def get_unseen_messages_count(obj,self):
        sender_id = obj.sender
        count = 0
        messages = Message.objects.filter(sender = sender_id )
        for m in messages:
            if m.is_read == False:
                count+=1
        return count
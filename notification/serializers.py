from rest_framework import serializers
from .models import Notification
from accounts.models import User


class NotificationSerializer(serializers.ModelSerializer):
    message = serializers.SerializerMethodField()
    sender_username = serializers.SerializerMethodField()
    sender_profile_photo_URL = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'user_sender', 'user_receiver', 'notif_type', 'is_seen', 'created_at', 'message', 'sender_username', 'sender_profile_photo_URL']

    def get_message(self, obj):
        sender = User.objects.get(id=obj.user_sender.id).username

        if obj.notif_type == 'like_post':
            return sender + ' liked your post.'
        elif obj.notif_type == 'offer_to_host':
            return sender + ' offered to become your host.'
        elif obj.notif_type == 'chosen_as_main_host':
            return sender + ' chose you as their host.'

    def get_sender_username(self, obj):
        sender = User.objects.get(id=obj.user_sender.id).username
        return sender

    def get_sender_profile_photo_URL(self, obj):
        sender = User.objects.get(id=obj.user_sender.id)

        if sender.profile_photo:
            return sender.profile_photo.url
        return None

from rest_framework import serializers
from .models import Like
from accounts.serializers import UserCompeleteProfileSerializer
from blog.serializers import BlogSerializer


class LikePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'

    def create(self, validated_data):
        validated_data['liker'] = self.context['request'].user
        validated_data['liked_post'] = self.context['post']
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance

class PostWithLikesSerializer(serializers.ModelSerializer):
    likers = serializers.SerializerMethodField()

    class Meta:
        model = Like
        fields = ['id', 'likers']


    def get_likers(self, obj):
        likers = Like
        if likers is not None:
            serializer = UserCompeleteProfileSerializer(likers, many=True)
            return serializer.data
        return likers

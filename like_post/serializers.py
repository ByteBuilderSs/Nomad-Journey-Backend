from rest_framework import serializers
from .models import Like


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
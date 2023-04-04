from rest_framework import serializers
from .models import AncRequest


class AncRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AncRequest
        fields = '__all__'

    def create(self, validated_data):
        validated_data['host'] = self.context['request'].user
        validated_data['req_anc'] = self.context['anc_id']
        instance = self.Meta.model(**validated_data)
        instance.save()
        return instance
from rest_framework import serializers
from .models import AncRequest


class AncRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = AncRequest
        fields = '__all__'
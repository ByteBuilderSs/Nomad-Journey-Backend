from rest_framework import serializers
from announcement.models import *
from blog.models import *
from feedback.models import *
from accounts.models import *

class MostRatedHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = ['']
from rest_framework.response import Response
from rest_framework.decorators import api_view
from datetime import datetime, timedelta
from .serializers import NotificationSerializer
from .models import Notification
from django.utils import timezone


@api_view(['GET'])
def UserNotifications(request, user_id):
    one_day_ago = datetime.now() - timedelta(days=1)
    one_day_ago = timezone.make_aware(one_day_ago, timezone.utc)
    notifs = Notification.objects.filter(user_receiver=user_id).filter(created_at__gte=one_day_ago)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def ChangeNotifToSeen(request, user_id):
    notifs = Notification.objects.filter(user_receiver=user_id).filter(is_seen=False)
    notifs.update(is_seen=True)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)

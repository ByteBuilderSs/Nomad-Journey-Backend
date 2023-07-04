from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import NotificationSerializer
from .models import Notification


@api_view(['GET'])
def UserNotifications(request, user_id):
    notifs = Notification.objects.filter(user_receiver=user_id).filter(is_seen=False)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def ChangeNotifToSeen(request, user_id):
    notifs = Notification.objects.filter(user_receiver=user_id).filter(is_seen=False)
    notifs.update(is_seen=True)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)

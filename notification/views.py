from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import NotificationSerializer
from .models import Notification


@api_view(['GET'])
def UserNotifications(request, user_id):
    notifs = Notification.objects.filter(user_receiver=user_id)
    serializer = NotificationSerializer(notifs, many=True)
    return Response(serializer.data)
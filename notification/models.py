from django.db import models
from accounts.models import User
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Notification(models.Model):
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_sender')
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_receiver')
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


def create_notification(sender, instance, created, **kwargs):
    if created:
        notification = Notification(user=instance.user, content='New notification')
        notification.save()

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'send_notification',
                'notification': {
                    'id': notification.id,
                    'content': notification.content,
                    'timestamp': str(notification.timestamp),
                }
            }
        )







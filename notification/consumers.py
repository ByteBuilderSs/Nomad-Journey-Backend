from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import sync_to_async, async_to_sync
from channels.layers import get_channel_layer
from accounts.models import User
from .models import Notification
import json



class NotificationConsumer(WebsocketConsumer):
    def connect(self):
        # if self.scope["user"].is_anonymous:
        #     self.close()
        # else:
            # kwargs = self.scope['url_route']['kwargs']

            # self.receiver_id = kwargs['receiver_id']

            async_to_sync(self.channel_layer.group_add)("Sample", self.channel_name)
            self.accept()


    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)("Sample", self.channel_name)


    def receive(self, text_data):
        async_to_sync(self.create_notification)(sender_id=1, receiver_id=2, message=text_data)


    def send_notification(self, event):
        notification = event['notification']

        self.send(json.dumps({
            'type': 'notification',
            'notification': notification
        }))


    @sync_to_async
    def create_notification(self, sender_id, receiver_id, message):
        sender = User.objects.get(id=sender_id)
        receiver = User.objects.get(id=receiver_id)

        notification = Notification.objects.create(
            user_sender=sender,
            user_receiver=receiver,
            message=message
        )

        channel_layer = get_channel_layer()

        async_to_sync(channel_layer.group_send)(
            "Sample",
            {
                'type': 'send_notification',
                'notification': {
                    'id': notification.id,
                    'user_sender': notification.user_sender.id,
                    'user_receiver': notification.user_receiver.id,
                    'message': notification.message,
                    'is_seen': notification.is_seen,
                    'created_at': notification.created_at.isoformat()
                },
            }
        )


    # def ChangeToSeen(request, notif_id):
    #     notification = Notification.objects.get(id=notif_id)
    #     notification.is_seen = True
    #     notification.save()

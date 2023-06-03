from django.db import models
from accounts.models import User


class Notification(models.Model):
    user_sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_sender')
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notif_receiver')
    message = models.CharField(max_length=255)
    is_seen = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message


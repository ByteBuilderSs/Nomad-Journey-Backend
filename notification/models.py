from django.db import models
from accounts.models import User


class Notification(models.Model):
    NOTIF_TYPE_CHOICES = (
        ('like_post', 'like_post'),
        ('offer_to_host', 'offer_to_host'),
        ('chosen_as_main_host', 'chosen_as_main_host')
    )

    user_sender = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='notif_sender', null=True)
    user_receiver = models.ForeignKey(User, on_delete=models.CASCADE, default=None, related_name='notif_receiver', null=True)
    notif_type = models.CharField(choices=NOTIF_TYPE_CHOICES, default=None, max_length=200)
    is_seen = models.BooleanField(null=True, blank=True, default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'This is a notification with id ' + str(self.id)
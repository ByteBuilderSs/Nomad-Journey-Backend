from django.db import models
from accounts.models import User
from announcement.models import Announcement

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    ans_id = models.ForeignKey(Announcement , on_delete=models.CASCADE , related_name='ans')
    def __str__(self):
        return self.message

    class Meta:
        ordering = ('created_at',)


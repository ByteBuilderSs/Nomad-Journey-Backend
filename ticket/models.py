from django.db import models
from accounts.models import User
from announcement.models import Announcement
# class Room(models.Model):
#     sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
#     receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')

class Message(models.Model):
    MESSAGE_TYPES = [
        ('sent', 'sent'),
        ('received', 'received')
    ]
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    type = models.CharField(max_length=10, choices=MESSAGE_TYPES)
    ans_id = models.ForeignKey(Announcement , on_delete=models.CASCADE , related_name='ans')
    # room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='messages')
    def __str__(self):
        return self.message

    class Meta:
        ordering = ('created_at',)


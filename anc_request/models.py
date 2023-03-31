from django.db import models
from accounts.models import User
from announcement.models import Announcement


class AncRequest(models.Model):
    host = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        default=None
    )
    req_anc = models.ForeignKey(
        Announcement,
        on_delete=models.CASCADE,
        default=None
    )
    req_description = models.TextField(max_length=500, null=True, blank=True)
    req_timestamp_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'This is a request with ID ' + str(self.id) + '.'
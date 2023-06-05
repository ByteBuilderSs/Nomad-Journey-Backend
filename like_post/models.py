from django.db import models
from accounts.models import User
from blog.models import Blog


class Like(models.Model):
    liker = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

    liked_post = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        default=None,
        null=True
    )

    like_timestamp_created = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('liked_post', 'liker')
    def __str__(self):
        return 'This is a like with ID ' + str(self.id) + '.'
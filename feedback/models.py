from django.db import models
from blog.models import Blog

class Feedback(models.Model):
    integer_choice = (
        (1, 'One'),
        (2, 'Two'),
        (3, 'Three'),
        (4, 'Four'),
        (5, 'Five'),
    )
    blog_id = models.ForeignKey(Blog , on_delete=models.SET_NULL)
    question_1 = models.IntegerField(choices=integer_choice)
    question_2 = models.IntegerField(choices=integer_choice)
    question_3 = models.IntegerField(choices=integer_choice)
    question_4 = models.IntegerField(choices=integer_choice)
    question_5 = models.IntegerField(choices=integer_choice)

# Create your models here.

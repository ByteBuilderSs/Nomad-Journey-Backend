from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from accounts.models import User
from announcement.models import Announcement

class Feedback(models.Model):
    question_1 = models.FloatField(validators=[MinValueValidator(1.0),MaxValueValidator(5.0)])
    question_2 = models.FloatField(validators=[MinValueValidator(1.0),MaxValueValidator(5.0)])
    question_3 = models.FloatField(validators=[MinValueValidator(1.0),MaxValueValidator(5.0)])
    question_4 = models.FloatField(validators=[MinValueValidator(1.0),MaxValueValidator(5.0)])
    question_5 = models.FloatField(validators=[MinValueValidator(1.0),MaxValueValidator(5.0)])
    user_id = models.ForeignKey(User , on_delete=models.CASCADE , related_name='feedback')
    ans_id = models.ForeignKey(Announcement , on_delete=models.CASCADE , related_name='feedback_ans')


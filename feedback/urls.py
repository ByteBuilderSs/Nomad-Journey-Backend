from django.urls import path
from .views import *


urlpatterns = [
    path('feedback-user/<str:username>' , FeedbackView.as_view()),
]
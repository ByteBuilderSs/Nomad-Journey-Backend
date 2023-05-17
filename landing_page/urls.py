from django.urls import path
from .views import *


urlpatterns = [path('most-rated-hosts' , MostRatedHost.as_view()),
]

#http://127.0.0.1:8000/api/v1/landing-page/most-rated-hosts
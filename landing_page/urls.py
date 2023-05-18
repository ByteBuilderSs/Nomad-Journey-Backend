from django.urls import path
from .views import *


urlpatterns = [ path('most-rated-hosts' , MostRatedHost.as_view()),
                path('most-visited-cities' , MostVisitedCities.as_view()),
                path('random-shit' , RandomShit.as_view())
]

#http://127.0.0.1:8000/api/v1/landing-page/most-rated-hosts
#http://127.0.0.1:8000/api/v1/landing-page/most-visited-cities
#http://127.0.0.1:8000/api/v1/landing-page/random-shit
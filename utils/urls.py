from django.urls import path
from .views import *


urlpatterns = [
    path('get-countries/', GetCountries),
    path('get-cities-of-country/<str:rec_id>', GetCitiesOfCountry),
    path('create-city/', CreateCity)
]

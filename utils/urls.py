from django.urls import path
from .views import *


urlpatterns = [
    path('get-countries/', GetCountries),
    path('get-cities-of-country/<str:rec_id>', GetCitiesOfCountry),
    path('get-all-cities/', GetAllCities),
    path('create-city/', CreateCity)
]

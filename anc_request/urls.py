from django.urls import path
from .views import *


urlpatterns = [
    path('get-requests-on-announcement/<str:anc_id>', GetRequestsOnAnnouncement),
    path('get-requests-of-host/<str:host_id>', GetRequestsOfHost),

    
]
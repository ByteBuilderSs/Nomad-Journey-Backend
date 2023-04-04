from django.urls import path
from .views import *


urlpatterns = [
    path('get-requests-on-announcement/<str:anc_id>', GetRequestsOnAnnouncement),
    path('get-requests-of-host/<str:host_id>', GetRequestsOfHost),

    path('create-request/<str:anc_id>', CreateRequest),

    path('accept-request/<str:req_id>', AcceptRequest),
    path('reject-request/<str:req_id>', RejectRequest)
]
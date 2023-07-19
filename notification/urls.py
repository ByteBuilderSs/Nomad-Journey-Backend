from django.urls import path
from .views import *

urlpatterns = [
    path('user-notifications/<str:user_id>', UserNotifications),
    path('change-notif-to-seen/<str:user_id>', ChangeNotifToSeen)
]
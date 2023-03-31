from django.urls import path
from .views import *


urlpatterns = [
    path('get-list/', GetAnnouncementList),
    path('get-announcements-for-host/', GetAnnouncementsForHost),
    path('get-single/<str:pk>/', GetSingleAnnouncement),
    path('create/', CreateAnnouncement),
    path('get-user-announcement/<str:username>', user_announcement),
    path('edit/<str:pk>/', EditAnnouncement),
    path('delete/<str:pk>/', DeleteAnnouncement)
]
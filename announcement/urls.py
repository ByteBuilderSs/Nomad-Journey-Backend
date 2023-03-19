from django.urls import path
from .views import *


urlpatterns = [
    path('get-list/', GetAnnouncementList),
    path('get-single/<str:pk>/', GetSingleAnnouncement),
    path('get-each-announcer/<str:fk>/' , GetAnnouncementListOfEachAnnouncer ),
    path('create/', CreateAnnouncement),
    path('edit/<str:pk>/', EditAnnouncement),
    path('delete/<str:pk>/', DeleteAnnouncement),
]
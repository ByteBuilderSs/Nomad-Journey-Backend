from django.urls import path
from .views import *


urlpatterns = [
    path('get-announcements-for-host/', GetAnnouncementsForHost),
    path('get-user-announcements/<str:username>', UserAnnouncements),
    path('user-announcements-more-details/', UserAnnouncementsMoreDetails),
    path('user-announcements-with-host-request/<str:user_id>', UserAnnouncementsWithHostRequest),

    path('create/', CreateAnnouncement),

    path('edit/<str:pk>/', EditAnnouncement),

    path('delete/<str:pk>/', DeleteAnnouncement),
    path('get-announcement-detail-by-id/<str:ans_id>' , GetAnnouncementDetailByAnnouncementId)

]
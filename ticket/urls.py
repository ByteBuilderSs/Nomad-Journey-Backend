from django.urls import path
from .views import *


urlpatterns = [
    # path('detail_message/<sender_username>/<receiver_username>/', AllMessageDetailView.as_view()),
    path('send_messages/<sender_username>/' , MessageGeneralListView.as_view()),
    path('messages/<sender_username>/<receiver_username>/',MessageGeneralListView.as_view() ),
    path('unseen-messages/<sender_username>/<receiver_username>/',MessageUnseenListView.as_view() ),
    path('get-all-messages/<sender_username>/<receiver_username>/' , AllMessageDetailView.as_view()),
    path('get-contacts/<username>/' , GetContacts.as_view()),
    path('get-contacts-volunteers/<username>/' , GetContactVolunteers.as_view()),
    path('get-contacts-requests/<username>/' , GetContactRequest.as_view()),
    path('all-unseen-messages/<sender_username>/' , AllMessageUnseenListView.as_view()),
]
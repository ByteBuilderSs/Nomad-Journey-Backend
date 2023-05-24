from django.urls import path
from .views import MessageGeneralListView , MessageUnseenListView


urlpatterns = [
    # path('detail_message/<sender_username>/<receiver_username>/', MessageDetailView.as_view()),
    path('send_messages/<sender_username>/' , MessageGeneralListView.as_view()),
    path('messages/<sender_username>/<receiver_username>/',MessageGeneralListView.as_view() ),
    path('unseen-messages/<sender_username>/<receiver_username>/',MessageUnseenListView.as_view() ),
]
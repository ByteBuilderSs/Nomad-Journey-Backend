from django.urls import path
from .views import MessageListView 


urlpatterns = [
    # path('detail_message/<sender_username>/<receiver_username>/', MessageDetailView.as_view()),
    path('send_messages/<sender_username>/' , MessageListView.as_view()),
    path('messages/<sender_username>/<receiver_username>/',MessageListView.as_view() ),
]
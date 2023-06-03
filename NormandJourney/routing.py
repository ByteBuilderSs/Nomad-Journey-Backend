from django.urls import path
from notification import consumers

urlpatterns = [
    path('notification/<int:receiver_id>', consumers.NotificationConsumer.as_asgi()),
    path('notification/', consumers.NotificationConsumer.as_asgi()),
]

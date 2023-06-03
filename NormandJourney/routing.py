from django.urls import path
from notification import consumers

urlpatterns = [
    path('ws/notifications/', consumers.NotificationConsumer.as_asgi()),
]

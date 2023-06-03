from django.urls import path
from notification import consumers

urlpatterns = [
    path('notification/', consumers.NotificationConsumer.as_asgi()),
]

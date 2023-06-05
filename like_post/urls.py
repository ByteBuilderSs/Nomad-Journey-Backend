from django.urls import path
from .views import *

urlpatterns = [
    path('create-like/<str:post_id>', CreateLike),
    path('get-likers/<str:post_id>', GetPostsWithLike),
    path('delete-like/<str:uid>/<str:liker>', DeleteLike)
]
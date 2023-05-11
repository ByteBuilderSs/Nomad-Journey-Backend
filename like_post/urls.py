from django.urls import path
from .views import *

urlpatterns = [
    path('create-like/<str:post_id>', CreateLike),
    path('get-posts-with-like/<str:post_id>', GetPostsWithLike)
]
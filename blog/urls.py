from django.urls import path
from .views import BlogView , BlogDetailView , TagView , PublicBlogView


urlpatterns = [
    path('posts/' , PublicBlogView.as_view()),
    path('userpost/' , BlogView.as_view()),
    path('post/<str:slug>' , BlogDetailView.as_view()),
    path('tags/' , TagView.as_view()),
]
from django.urls import path
from .views import RegisterView, UserLoginView, UserView, LogoutView, UserProfileList, UserProfileDetail

urlpatterns = [
    path('register/' , RegisterView.as_view()),
    path('login/' , UserLoginView.as_view()),
    path('login-user/' , UserView.as_view()),
    path('logout/' , LogoutView.as_view()),
    path('users/' , UserProfileList.as_view()),
    path('user/<str:username>/', UserProfileDetail.as_view()),
]
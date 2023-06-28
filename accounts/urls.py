from django.urls import path
from .views import *
from rest_framework_simplejwt import views as jwt_views
from .token_view import MyTokenObtainPairView

urlpatterns = [
    path('register/' , RegisterView.as_view()),
    path('login/' , LoginView.as_view()),
    path('login-user/' , UserView.as_view()),
    path('logout/' , LogoutView.as_view()),
    # path('users/' , UserProfileList.as_view()),
    path('user/<str:username>/', UserProfileDetail.as_view()),
    # urls for token APIs
    # path('token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path("token/", MyTokenObtainPairView.as_view(), name="my_token_obtain_pair"),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('UserProfileEdit1/<str:username>' , UserProfileEdit1.as_view()),
    path('UserProfileEdit2/<str:username>' , UserProfileEdit2.as_view()),
    path('UserProfileEdit3/<str:username>' , UserProfileEdit3.as_view()),
    path('UserProfileEdit4/<str:username>' , UserProfileEdit4.as_view()),
    path('UserProfileEdit5/<str:username>' , UserProfileEdit5.as_view()),
    # path('GetUsernameAndUserImageByUserId/<str:id>' , GetUsernameAndUserImageByUserId.as_view()),
    path('GetUserProfileForOverview/<str:username>', GetUserProfileForOverview.as_view()),
    path('GetLanguages', LanguageView.as_view()),
    path('get-profile-photo/<str:user_id>', ProfilePhoto.as_view()),
    path('add-coin/<str:username>', AddCoin.as_view()),
    path('get-users-requests-announcer/<str:username>' , GetUsersRequestsAnnouncer.as_view()),
    path('UserProfileEdit6/<str:username>' , UserProfileEdit6.as_view()),
    path('UserProfileEdit7/<str:username>' , UserProfileEdit7.as_view()),
    path('UserProfileEdit8/<str:username>' , UserProfileEdit8.as_view()),
    path('UserProfileEdit9/<str:username>' , UserProfileEdit9.as_view()),
    path('UserProfileEdit10/<str:username>' , UserProfileEdit10.as_view()),
]
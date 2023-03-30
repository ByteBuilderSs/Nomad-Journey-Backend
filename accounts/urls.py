from django.urls import path
from .views import RegisterView, LoginView,UserView,LogoutView,UserProfileList,UserProfileDetail,UserProfileEdit1,UserProfileEdit2
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
]
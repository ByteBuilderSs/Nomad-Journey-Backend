from rest_framework_simplejwt.views import TokenViewBase
from .token_serializer import MyTokenObtainPairSerializer

class MyTokenObtainPairView(TokenViewBase):
    """
    Takes a set of user credentials and returns an access and refresh JSON web
    token pair to prove the authentication of those credentials.
    """
    serializer_class = MyTokenObtainPairSerializer
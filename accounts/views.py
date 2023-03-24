from rest_framework.views import APIView
from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserLoginSerializer, UserSerializer , UserCompeleteProfileSerializer
from .models import User
import jwt , datetime
from django.shortcuts import get_object_or_404
import json
from NormandJourney.tools import hash_sha256
from rest_framework_simplejwt.tokens import RefreshToken

# from rest_framework_jwt.authentication import JSONWebTokenAuthentication

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        if request.method == "POST":
            try:
                body = json.loads(request.body.decode('utf-8'))
                serializer = UserSerializer(data=body)
                serializer.is_valid(raise_exception=True)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
            except:
                return Response({"message": "Something went wrong:("}, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = (AllowAny, )
    def post(self, request):
        if request.method == "POST":
            try:
                body = json.loads(request.body.decode('utf-8'))

                email = body['email']
                password = body['password']

                user = User.objects.filter(email = email).first()

                if user is None:
                    raise AuthenticationFailed('User not found!')
                
                if not user.check_password(password):
                    raise AuthenticationFailed('Incorrect password!')
                
                payload = {
                    'id': user.id,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=2),
                    'iat': datetime.datetime.utcnow()
                }
                
                token = jwt.encode(payload, 'secret', algorithm='HS256').decode('utf-8')

                response = Response()
                response.status_code = status.HTTP_200_OK
                response.set_cookie(key='jwt', value=token, httponly=True)
                response.data = {
                    'jwt': token,
                    'username': user.username
                }
                return response
            except:
                return Response({"message": "Something went wrong"}, status=status.HTTP_400_BAD_REQUEST)

# class UserLoginView(APIView):
#     permission_classes = (AllowAny,)
#     serializer_class = UserLoginSerializer
#     def post(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         response = {
#             'success' : 'True',
#             'status code' : status.HTTP_200_OK,
#             'message': 'User logged in  successfully',
#             'token' : serializer.data['token'],
#             }
#         status_code = status.HTTP_200_OK

#         return Response(response, status=status_code)

class UserView(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self , request):
        if request.method == "GET":
            # try:
            token = request.COOKIES.get('jwt')
            
            if not token:
                raise AuthenticationFailed('Unauthenticated')
            
            try:
                payload = jwt.decode(token , 'secret' , algorithm=['HS256'])
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed('Unauthenticated')
            
            user = User.objects.filter(id = payload['id']).first()
            serializer = UserCompeleteProfileSerializer(user)
            return Response(serializer.data)
            # except:
                # return Response({"message" : "Unable to load user info"}, status=status.HTTP_400_BAD_REQUEST)
    
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self , request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCompeleteProfileSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
    
class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserCompeleteProfileSerializer
    def get_object(self):
        UserName= self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)
    

class UserProfileView(APIView):

    permission_classes = (IsAuthenticated,)
    # authentication_class = JSONWebTokenAuthentication

    def get(self, request):
        try:
            user_profile = User.objects.get(user=request.user)
            status_code = status.HTTP_200_OK
            response = {
                'success': 'true',
                'status code': status_code,
                'message': 'User profile fetched successfully',
                'data': [{
                    'first_name': user_profile.first_name,
                    'last_name': user_profile.last_name,
                    'phone_number': user_profile.phone_number,
                    'age': user_profile.age,
                    'gender': user_profile.gender,
                    }]
                }

        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
                }
        return Response(response, status=status_code)








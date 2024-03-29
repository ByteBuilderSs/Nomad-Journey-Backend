from rest_framework.views import APIView
from rest_framework import generics , status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import AuthenticationFailed
from .serializers import *
from .models import User
from utils.models import *
from anc_request.models import *
from announcement.models import Announcement
from blog.models import Blog
from .permissions import IsOwner
import jwt , datetime
from django.shortcuts import get_object_or_404
import json
from rest_framework.exceptions import NotFound
from NormandJourney.tools import hash_sha256
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.parsers import MultiPartParser
from django.contrib.auth.hashers import make_password ,check_password
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

def generate_reset_token(user):
    payload = {
        'user_id': user.id,
        'email': user.email,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)  # تاریخ انقضای توکن: 24 ساعت بعد از زمان فعلی
    }
    token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
    return token.decode('utf-8')


def calculate_expiry_date():
    return timezone.now() + timedelta(hours=72)

def send_reset_email(email, reset_token):
    subject = 'Password Reset'
    # message = f'Click the link to reset your password: http://188.121.102.52:8000/api/v1/accounts/reset?token={reset_token}'
    message = f'Click the link to reset your password: http://localhost:3000/resetpass?token={reset_token}'
    sender_email = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, sender_email, recipient_list)

class ResetPasswordPageView(APIView):
    def get(self, request):
        reset_token = request.GET.get('token', '')

        user_model = get_user_model()
        user = get_object_or_404(user_model, reset_token=reset_token)

        return Response({"reset_token": reset_token})

    def post(self, request):
        password = request.data.get('password', '')
        user_model = get_user_model()
        user = get_object_or_404(user_model, reset_token=request.data.get('reset_token', ''))

        user.set_password(password)
        user.reset_token = ''
        user.save()

        return Response(status=status.HTTP_200_OK)

class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        if request.method == "POST":
            # try:
            body = json.loads(request.body.decode('utf-8'))
            serializer = UserSerializer(data=body)
            serializer.is_valid(raise_exception=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors , status = status.HTTP_400_BAD_REQUEST)
            # except:
            #     return Response({"message": "Something went wrong:("}, status=status.HTTP_400_BAD_REQUEST)

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

class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise NotFound('User not found')

        # Generate reset token
        reset_token = generate_reset_token(user)
        expiry_date = calculate_expiry_date()

        # Update user model with reset token and expiry
        user.reset_token = reset_token
        user.reset_token_expiry = expiry_date
        user.save()

        # Send email with reset link
        send_reset_email(user.email, reset_token)

        return Response({'message': 'Password reset email sent'})

class UserView(APIView):
    permission_classes=(IsAuthenticated,)
    def get(self , request):
        if request.method == "GET":
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

class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self , request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({
                'data': {},
                'message': "logout successfully"
            }, status=status.HTTP_200_OK)
        except:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
class UserProfileList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserCompeleteProfileSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        return queryset
    
class UserProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsOwner,)
    queryset = User.objects.all()
    serializer_class = UserCompeleteProfileSerializer
    def get_object(self):
        UserName= self.kwargs.get("username")
        return get_object_or_404(User, username=UserName)


class UserProfileEdit1(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )

            if body.get('first_name') is None:
                return Response({
                    'data': {},
                    'message':'firstname should not be null'
                }, status = status.HTTP_400_BAD_REQUEST )
            if body.get('last_name')  is None:
                return Response({
                    'data': {},
                    'message':'lastname should not be null'
                }, status = status.HTTP_400_BAD_REQUEST )
            if body.get('username')  is None:
                return Response({
                    'data': {},
                    'message':'username should not be null'
                }, status = status.HTTP_400_BAD_REQUEST )
            serializer = UserProfileEdit1Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


class UserProfileEdit2(APIView):
    def patch(self , request , username):
        # try:
        body = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username = username)
        if len(user) == 0:
            return Response({
                'data': {},
                'message':'invalid username'
            }, status = status.HTTP_400_BAD_REQUEST )
        if request.user.id != user[0].id:
            return Response({
                'data': {},
                'message':'you are not authorized to do this'
            }, status = status.HTTP_400_BAD_REQUEST )

        # if body.get('User_city') is None:
        #     return Response({
        #         'data': {},
        #         'message':'city field should not be null'
        #     }, status = status.HTTP_400_BAD_REQUEST )
        # if body.get('User_country')  is None:
        #     return Response({
        #         'data': {},
        #         'message':'country field should not be null'
        #     }, status = status.HTTP_400_BAD_REQUEST )
        if body.get('User_postal_code')  is None:
            return Response({
                'data': {},
                'message':'postal code field should not be null'
            }, status = status.HTTP_400_BAD_REQUEST )
        serializer = UserProfileEdit2Serializer(user[0] , data = body , partial = True)
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message':'something went wrong'
            } , status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'data': serializer.data,
            'message' : 'user updated successfully'
        } , status = status.HTTP_201_CREATED)
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )

class UserProfileEdit3(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if body.get('interests') is not None:
                for i in body['interests']:
                    interst_id = UserInterest.objects.filter(interest_name = i)
                    if len(interst_id) == 0:
                        UserInterest.objects.create(interest_name = i)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )

            serializer = UserProfileEdit3Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class UserProfileEdit4(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileEdit4Serializer
    parser_classes = [MultiPartParser]
    lookup_field = 'username'

    # def patch(self, request, username):
    #     user = User.objects.get(username=username)
    #     serializer = self.get_serializer(user, data=request.data, partial=True)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)

    #     return Response(serializer.data)

        # try:
        #     body = json.loads(request.body.decode('utf-8'))
        #     user = User.objects.filter(username = username)
        #     if len(user) == 0:
        #         return Response({
        #             'data': {},
        #             'message':'invalid username'
        #         }, status = status.HTTP_400_BAD_REQUEST )
        #     if request.user.id != user[0].id:
        #         return Response({
        #             'data': {},
        #             'message':'you are not authorized to do this'
        #         }, status = status.HTTP_400_BAD_REQUEST )

        #     serializer = UserProfileEdit4Serializer(user[0] , data = body , partial = True)
        #     if not serializer.is_valid():
        #         return Response({
        #             'data': serializer.errors,
        #             'message':'something went wrong'
        #         } , status = status.HTTP_400_BAD_REQUEST)
        #     serializer.save()
        #     return Response({
        #         'data': serializer.data,
        #         'message' : 'user updated successfully'
        #     } , status = status.HTTP_201_CREATED)
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )

    def delete(self , request , username):
        try:
            user = User.objects.get(username = username)
            if user is None:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.username != username:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            if user.profile_photo is None:
                return Response({
                    'data': {},
                    'message':'there is no image to be deleted'
                }, status = status.HTTP_400_BAD_REQUEST )
            user.profile_photo = None
            user.save()
            return Response({
                'data':{},
                'message' : 'image deleted successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class UserProfileEdit5(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            serializer = UserProfileEdit5Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )
    def get(self , request , username):
        try:
            user= User.objects.get(username = username)
            serializer = UserProfileEdit5Serializer(user)
            return Response({
                'data':serializer.data,
                'message' : 'user info fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class UserProfileEdit6(APIView):
    def patch(self , request , username):
        body = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username = username)
        if len(user) == 0:
            return Response({
                'data': {},
                'message':'invalid username'
            }, status = status.HTTP_400_BAD_REQUEST )
        if request.user.id != user[0].id:
            return Response({
                'data': {},
                'message':'you are not authorized to do this'
            }, status = status.HTTP_400_BAD_REQUEST )
        if body.get('User_postal_code')  is None:
            return Response({
                'data': {},
                'message':'postal code field should not be null'
            }, status = status.HTTP_400_BAD_REQUEST )
        serializer = UserProfileEdit6Serializer(user[0] , data = body , partial = True)
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message':'something went wrong'
            } , status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'data': serializer.data,
            'message' : 'user updated successfully'
        } , status = status.HTTP_201_CREATED)


class UserProfileEdit7(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            serializer = UserProfileEdit7Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )
    def get(self , request , username):
        try:
            user= User.objects.get(username = username)
            serializer = UserProfileEdit7Serializer(user)
            return Response({
                'data':serializer.data,
                'message' : 'user info fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


class UserProfileEdit8(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            serializer = UserProfileEdit8Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )
    def get(self , request , username):
        try:
            user= User.objects.get(username = username)
            serializer = UserProfileEdit8Serializer(user)
            return Response({
                'data':serializer.data,
                'message' : 'user info fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class UserProfileEdit9(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            if not check_password(body['old_password'] , user[0].password):
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            user[0].password = make_password(body['new_password'])
            user[0].password_again = hash_sha256(body['new_password'])
            user[0].save()
            serializer = UserProfileEdit9Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class UserProfileEdit10(APIView):
    def patch(self , request , username):
        try:
            body = json.loads(request.body.decode('utf-8'))
            user = User.objects.filter(username = username)
            if len(user) == 0:
                return Response({
                    'data': {},
                    'message':'invalid username'
                }, status = status.HTTP_400_BAD_REQUEST )
            if request.user.id != user[0].id:
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            if not check_password(body['password'] , user[0].password):
                return Response({
                    'data': {},
                    'message':'you are not authorized to do this'
                }, status = status.HTTP_400_BAD_REQUEST )
            user[0].email = body['new_email']
            user[0].save()
            serializer = UserProfileEdit9Serializer(user[0] , data = body , partial = True)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message':'something went wrong'
                } , status = status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response({
                'data': serializer.data,
                'message' : 'user updated successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )


# class GetUsernameAndUserImageByUserId(APIView):
#     def get(self,request , id):
#         user = get_object_or_404(User, id=id)
#         serializer = GetUsernameAndUserImageByUserIdSerializer(user)
#         return Response(serializer.data)

class GetUserProfileForOverview(APIView):
    def get(self , request,username):
        # try:
        information = User.objects.filter(username = username)
        if  not information.exists():
            return Response({
                'data': {},
                'message':'invalid username'
            }, status = status.HTTP_400_BAD_REQUEST )
        serializer = UserProfileForOverviewSerializer(information[0])
        return Response({
            'data':serializer.data,
            'message' : 'user information fetched successfully'
        } , status = status.HTTP_200_OK)
        # except Exception as e:
        #     print(e) 
        #     return Response({
        #         'data': {},
        #         'message':'something went wrong'
        #     }, status = status.HTTP_400_BAD_REQUEST )

class LanguageView(APIView):
    def get(self , request):
        try:
            language = Language.objects.all()
            serializer = LanguageSerializer(language , many = True)
            return Response({
                'data':serializer.data,
                'message' : 'language fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )

class ProfilePhoto(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        if user.profile_photo is None:
            return Response("aysa")
        serializer = UserProfilePhotoSerializer(user)
        return Response(serializer.data)

class AddCoin(APIView):
    def put(self , request , username):
        body = json.loads(request.body.decode('utf-8'))
        user = User.objects.filter(username = username)
        if len(user) == 0:
            return Response({
                'data': {},
                'message':'invalid username'
            }, status = status.HTTP_400_BAD_REQUEST )
        user[0].coins = user[0].coins + int(body['coin_to_buy'])
        user[0].save()
        if request.user.id != user[0].id:
            return Response({
                'data': {},
                'message':'you are not authorized to do this'
            }, status = status.HTTP_400_BAD_REQUEST )
        serializer = UserAddCoinSerializerPut(user[0] , data = body , partial = True)
        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message':'something went wrong'
            } , status = status.HTTP_400_BAD_REQUEST)
        serializer.save()
        return Response({
            'data': serializer.data,
            'message' : 'coins added successfully'
        } , status = status.HTTP_201_CREATED)
    def get(self , request , username):
        try:
            user= User.objects.get(username = username)
            serializer = UserAddCoinSerializerGet(user)
            return Response({
                'data':serializer.data,
                'message' : 'user coins and price fetched successfully'
            } , status = status.HTTP_201_CREATED)
        except Exception as e:
            print(e) 
            return Response({
                'data': {},
                'message':'something went wrong'
            }, status = status.HTTP_400_BAD_REQUEST )
        

class GetUsersRequestsAnnouncer(APIView):
    def get(self , request , username):
        user_id = User.objects.get(username = username).id
        requests = AncRequest.objects.filter(host = user_id )
        announcers_requested = []
        for re in requests:
            ans = Announcement.objects.get(id = re.req_anc.id)
            announcers_requested.append(User.objects.get(id = ans.announcer.id))
        announcers_requested = list(set(announcers_requested))
        serializer = UserCompeleteProfileSerializer(announcers_requested ,  many=True)
        return Response({
            'data':serializer.data,
            'message' : 'users fetched successfully'
        } , status = status.HTTP_201_CREATED)
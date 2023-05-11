from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import PasswordField
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login
from django.utils.translation import gettext_lazy as _

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = get_user_model().USERNAME_FIELD

    default_error_messages = {
        'no_active_account': _('No active account found with the given credentials')
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields[self.username_field] = serializers.CharField(
            default=None, allow_blank=True)
        self.fields['password'] = PasswordField()
        self.fields['email'] = serializers.EmailField(
            default=None, allow_blank=True)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def super_validate(self, attrs):
        authenticate_kwargs = {
            self.username_field: None if attrs[self.username_field] == "" else attrs[self.username_field],
            'password': attrs['password'],
            'email': None if attrs['email'] == "" else attrs['email'],
        }
        try:
            authenticate_kwargs['request'] = self.context['request']
        except KeyError:
            pass

        self.user = authenticate(**authenticate_kwargs)

        if not api_settings.USER_AUTHENTICATION_RULE(self.user):
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        return {}

    def validate(self, attrs):
        data = self.super_validate(attrs)

        refresh = self.get_token(self.user)

        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data.update({'username': self.user.username})
        data.update({'user_id': self.user.id})
        data.update({'user_city': self.user.User_city.id})
        data.update({'user_profile_photo' : self.user.profile_photo.url})
        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data

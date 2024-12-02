from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from BackendTennis.trads.auth_message import AUTH_MESSAGES


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_staff'] = user.is_staff

        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)
        except AuthenticationFailed as e:
            raise AuthenticationFailed(_(AUTH_MESSAGES['ERROR']['INVALID_EMAIL_OR_PASSWORD']))

        user = self.user
        if not user.is_active:
            raise AuthenticationFailed(_(AUTH_MESSAGES['ERROR']['INACTIVE_ACCOUNT']))

        return data

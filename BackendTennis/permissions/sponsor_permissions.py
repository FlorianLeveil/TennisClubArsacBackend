from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

from BackendTennis.models import Sponsor
from BackendTennis.permissions.BasePermission import BasePermissions


class SponsorPermissions(BasePermissions):
    model_name = Sponsor.__name__.lower()
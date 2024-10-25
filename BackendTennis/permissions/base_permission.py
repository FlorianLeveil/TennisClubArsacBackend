from rest_framework import permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from BackendTennis.models import Category


class BasePermissions(permissions.BasePermission):
    model_name = None

    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True

        jwt_auth = JWTAuthentication()
        try:
            user_auth_tuple = jwt_auth.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple  # Unpack user and token data
            else:
                return False
        except AuthenticationFailed:
            return False

        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            if not request.user.is_authenticated:
                return False

            model_perms = {
                'POST': f'add_{self.model_name}',
                'PUT': f'change_{self.model_name}',
                'PATCH': f'change_{self.model_name}',
                'DELETE': f'delete_{self.model_name}',
            }

            perm = model_perms.get(request.method, None)
            if perm and request.user.has_perm(f'BackendTennis.{perm}'):
                return True
            if request.user.is_superuser:
                return True

        return False

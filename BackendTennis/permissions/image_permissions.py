from BackendTennis.models import Image
from BackendTennis.permissions.BasePermission import BasePermissions


class ImagePermissions(BasePermissions):
    model_name = Image.__name__.lower()

from BackendTennis.models import Image
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class ImagePermissions(BasePermissions):
    model_name = Image.__name__.lower()

from BackendTennis.models import Render
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class RenderPermissions(BasePermissions):
    model_name = Render.__name__.lower()

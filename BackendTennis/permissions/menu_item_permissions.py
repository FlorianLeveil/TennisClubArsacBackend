from BackendTennis.models import MenuItem
from BackendTennis.permissions.base_permission import BasePermissions


class MenuItemPermissions(BasePermissions):
    model_name = MenuItem.__name__.lower()

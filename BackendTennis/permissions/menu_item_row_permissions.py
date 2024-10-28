from BackendTennis.models import MenuItemRow
from BackendTennis.permissions.base_permission import BasePermissions


class MenuItemRowPermissions(BasePermissions):
    model_name = MenuItemRow.__name__.lower()

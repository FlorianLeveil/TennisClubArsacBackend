from BackendTennis.models import NavigationItem
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class NavigationItemPermissions(BasePermissions):
    model_name = NavigationItem.__name__.lower()

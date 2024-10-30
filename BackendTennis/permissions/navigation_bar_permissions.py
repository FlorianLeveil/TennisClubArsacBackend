from BackendTennis.models import NavigationBar
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class NavigationBarPermissions(BasePermissions):
    model_name = NavigationBar.__name__.lower()

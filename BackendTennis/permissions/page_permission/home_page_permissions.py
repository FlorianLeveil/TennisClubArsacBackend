from BackendTennis.models import HomePage
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class HomePagePermissions(BasePermissions):
    model_name = HomePage.__name__.lower()

from BackendTennis.models import Route
from BackendTennis.permissions.base_permission import BasePermissions


class RoutePermissions(BasePermissions):
    model_name = Route.__name__.lower()

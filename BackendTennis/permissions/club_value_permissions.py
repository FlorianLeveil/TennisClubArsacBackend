from BackendTennis.models import ClubValue
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class ClubValuePermissions(BasePermissions):
    model_name = ClubValue.__name__.lower()

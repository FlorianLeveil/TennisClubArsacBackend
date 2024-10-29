from BackendTennis.models import TeamPage
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class TeamPagePermissions(BasePermissions):
    model_name = TeamPage.__name__.lower()

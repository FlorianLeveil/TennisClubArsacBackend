from BackendTennis.models import TeamPage
from BackendTennis.permissions.BasePermission import BasePermissions


class TeamPagePermissions(BasePermissions):
    model_name = TeamPage.__name__.lower()

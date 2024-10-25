from BackendTennis.models import Tournament
from BackendTennis.permissions.BasePermission import BasePermissions


class TournamentPermissions(BasePermissions):
    model_name = Tournament.__name__.lower()

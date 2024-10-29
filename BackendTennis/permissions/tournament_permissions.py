from BackendTennis.models import Tournament
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class TournamentPermissions(BasePermissions):
    model_name = Tournament.__name__.lower()

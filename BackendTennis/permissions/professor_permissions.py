from BackendTennis.models import Professor
from BackendTennis.permissions.BasePermission import BasePermissions


class ProfessorPermissions(BasePermissions):
    model_name = Professor.__name__.lower()

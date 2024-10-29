from BackendTennis.models import Professor
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class ProfessorPermissions(BasePermissions):
    model_name = Professor.__name__.lower()

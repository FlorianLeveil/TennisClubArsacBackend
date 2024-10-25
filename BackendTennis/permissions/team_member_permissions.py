from BackendTennis.models import TeamMember
from BackendTennis.permissions.base_permission import BasePermissions


class TeamMemberPermissions(BasePermissions):
    model_name = TeamMember.__name__.lower()

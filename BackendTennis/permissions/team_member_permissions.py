from BackendTennis.models import TeamMember
from BackendTennis.permissions.BasePermission import BasePermissions


class TeamMemberPermissions(BasePermissions):
    model_name = TeamMember.__name__.lower()

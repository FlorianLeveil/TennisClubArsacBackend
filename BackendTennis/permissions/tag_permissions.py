from BackendTennis.models import Tag
from BackendTennis.permissions.BasePermission import BasePermissions


class TagPermissions(BasePermissions):
    model_name = Tag.__name__.lower()

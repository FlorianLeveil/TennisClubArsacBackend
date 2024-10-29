from BackendTennis.models import Tag
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class TagPermissions(BasePermissions):
    model_name = Tag.__name__.lower()

from BackendTennis.models import News
from BackendTennis.permissions.BasePermission import BasePermissions


class NewsPermissions(BasePermissions):
    model_name = News.__name__.lower()

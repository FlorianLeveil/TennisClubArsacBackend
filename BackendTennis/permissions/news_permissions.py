from BackendTennis.models import News
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class NewsPermissions(BasePermissions):
    model_name = News.__name__.lower()

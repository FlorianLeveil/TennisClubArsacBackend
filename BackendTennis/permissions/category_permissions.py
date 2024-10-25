from BackendTennis.models import Category
from BackendTennis.permissions.BasePermission import BasePermissions


class CategoryPermissions(BasePermissions):
    model_name = Category.__name__.lower()

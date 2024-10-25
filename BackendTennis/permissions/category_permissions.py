from BackendTennis.models import Category
from BackendTennis.permissions.base_permission import BasePermissions


class CategoryPermissions(BasePermissions):
    model_name = Category.__name__.lower()

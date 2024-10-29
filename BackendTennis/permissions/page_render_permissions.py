from BackendTennis.models import PageRender
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class PageRenderPermissions(BasePermissions):
    model_name = PageRender.__name__.lower()

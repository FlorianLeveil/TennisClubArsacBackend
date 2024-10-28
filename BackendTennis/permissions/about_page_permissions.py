from BackendTennis.models import AboutPage
from BackendTennis.permissions.base_permission import BasePermissions


class AboutPagePermissions(BasePermissions):
    model_name = AboutPage.__name__.lower()

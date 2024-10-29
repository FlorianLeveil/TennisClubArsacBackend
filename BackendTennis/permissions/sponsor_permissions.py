from BackendTennis.models import Sponsor
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class SponsorPermissions(BasePermissions):
    model_name = Sponsor.__name__.lower()

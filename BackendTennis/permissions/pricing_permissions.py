from BackendTennis.models import Pricing
from BackendTennis.permissions.base_permission import BasePermissions


class PricingPermissions(BasePermissions):
    model_name = Pricing.__name__.lower()

from BackendTennis.models import Pricing
from BackendTennis.permissions.BasePermission import BasePermissions


class PricingPermissions(BasePermissions):
    model_name = Pricing.__name__.lower()

from BackendTennis.models import PricingPage
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class PricingPagePermissions(BasePermissions):
    model_name = PricingPage.__name__.lower()

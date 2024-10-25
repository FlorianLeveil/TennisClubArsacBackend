from BackendTennis.models import Event
from BackendTennis.permissions.BasePermission import BasePermissions


class EventPermissions(BasePermissions):
    model_name = Event.__name__.lower()

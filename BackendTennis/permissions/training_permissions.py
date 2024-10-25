from BackendTennis.models import Training
from BackendTennis.permissions.BasePermission import BasePermissions


class TrainingPermissions(BasePermissions):
    model_name = Training.__name__.lower()

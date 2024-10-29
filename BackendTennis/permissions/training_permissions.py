from BackendTennis.models import Training
from BackendTennis.permissions.base_permission.base_permission import BasePermissions


class TrainingPermissions(BasePermissions):
    model_name = Training.__name__.lower()

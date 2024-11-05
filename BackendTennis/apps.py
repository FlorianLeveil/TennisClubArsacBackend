from django.apps import AppConfig


class BackendtennisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'BackendTennis'

    def ready(self):
        import BackendTennis.signals

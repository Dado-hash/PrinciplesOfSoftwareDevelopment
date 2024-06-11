from django.apps import AppConfig


class FreshtrackConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'freshtrack'

    def ready(self):
            import freshtrack.signals
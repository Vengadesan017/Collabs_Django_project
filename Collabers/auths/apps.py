from django.apps import AppConfig


class AuthsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'auths'

    def ready(self):
        import auths.signals  # this connects your signal handler
        # import Collabers.auths.utils  # ensure utility functions are loaded
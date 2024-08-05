# your_app/apps.py

from django.apps import AppConfig

class YourAppConfig(AppConfig):
    name = 'apps.home'

    def ready(self):
        import apps.home.signals  # Ensure signals are imported
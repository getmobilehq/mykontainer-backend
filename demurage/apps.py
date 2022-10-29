from django.apps import AppConfig


class DemurageConfig(AppConfig):
    name = 'demurage'


    def ready(self):
        import demurage.signals
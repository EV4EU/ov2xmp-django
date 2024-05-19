from django.apps import AppConfig


class OcpiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ocpi'

    def ready(self):
        import ov2xmp.schema

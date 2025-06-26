from django.apps import AppConfig


class ConnectorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'connector'
    
    def ready(self):
        import connector.signals

from django.apps import AppConfig

class ProveedorConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Proveedor'

    def ready(self):
        import Proveedor.signals  # Importa el archivo de señales

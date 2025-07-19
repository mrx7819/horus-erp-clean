from django.apps import AppConfig


class InventarioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Inventario'

    def ready(self):
        import Inventario.signals  # Importa las señales

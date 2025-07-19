from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProveedorViewSet

# Crear un enrutador para las rutas de DRF
router = DefaultRouter()
router.register(r'proveedores', ProveedorViewSet, basename='proveedor')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el enrutador
]

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoriaViewSet, BodegaViewSet

# Configurar el enrutador para las vistas
router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet, basename='categoria')
router.register(r'bodegas', BodegaViewSet, basename='bodega')

urlpatterns = [
    path('', include(router.urls)),  # Incluye las rutas generadas por el enrutador
]

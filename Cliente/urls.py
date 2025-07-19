from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ClienteViewSet, InteraccionClienteViewSet, ClienteConInteraccionViewSet

router = DefaultRouter()
router.register(r'clientes', ClienteViewSet, basename='cliente')  # Rutas para Cliente
router.register(r'interacciones', InteraccionClienteViewSet, basename='interaccion-cliente')  # Rutas para Interacciones
router.register(r'clientes-con-interacciones', ClienteConInteraccionViewSet, basename='cliente-con-interacciones')  # Combinado (Opcional)

urlpatterns = [
    path('', include(router.urls)),
]

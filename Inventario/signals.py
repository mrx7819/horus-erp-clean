from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Producto, Bodega
from Venta.models import Detalle_Venta


@receiver(post_delete, sender=Producto)
def actualizar_cantidad_bodega_al_eliminar(sender, instance, **kwargs):
    """
    Resta la cantidad de productos de la bodega cuando se elimina un producto.
    """
    bodega = instance.bodega
    nueva_cantidad = (bodega.cantidad_art or 0) - instance.cantidad
    bodega.cantidad_art = max(nueva_cantidad, 0)  # Asegurarse de no ser negativa
    bodega.save()



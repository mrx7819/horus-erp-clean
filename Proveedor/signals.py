from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Detalle_Pedido

@receiver([post_save, post_delete], sender=Detalle_Pedido)
def actualizar_total_pedido(sender, instance, **kwargs):
    pedido = instance.pedido
    pedido.calcular_total()

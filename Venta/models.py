from django.db import models
from Cliente.models import Cliente
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
# Nota: No importamos Producto directamente para evitar la importación circular.

class Venta(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
        ('Otro', 'Otro'),
    ]
    metodo_pago = models.CharField(max_length=20, choices=METODO_PAGO_CHOICES)

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Venta {self.id} - {self.cliente.nombre} {self.cliente.apellido} - {self.fecha_creacion}"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"
        db_table = "venta"
        ordering = ["-fecha_creacion"]


class Detalle_Venta(models.Model):
    venta = models.ForeignKey(Venta, on_delete=models.CASCADE)
    producto = models.ForeignKey('Inventario.Producto', on_delete=models.PROTECT)
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    descuento = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_venta = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)  # Se calcula automáticamente
    fecha_creacion = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    def calcular_subtotal(self):
        """
        Calcula el subtotal aplicando el descuento.
        """
        subtotal = self.cantidad * self.precio_unitario
        total_final = subtotal * (1 - (self.descuento / 100))
        return max(total_final, 0)

    def save(self, *args, **kwargs):
        """
        Sobrescribir el método save para calcular automáticamente el total de la venta.
        """
        self.total_venta = self.calcular_subtotal()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Detalle de Venta {self.id} - Producto: {self.producto.nombre} - Cantidad: {self.cantidad}"

    class Meta:
        verbose_name = "Detalle de Venta"
        verbose_name_plural = "Detalles de Ventas"
        db_table = "detalle_venta"
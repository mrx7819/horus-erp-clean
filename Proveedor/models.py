from django.db import models
from Ubicacion.models import *
from Inventario import *
from django.utils.text import slugify  # Importar slugify para generar slugs automáticamente
from django.contrib.auth.models import User
from django.conf import settings
from django.utils import timezone

class CategoriaGiro(models.Model):
    nombre = models.CharField(max_length=150)

    def __str__(self):
        return self.nombre
    class Meta:
        db_table = 'categoria_giro'  # Nombre de la tabla en la base de datos
        ordering = ['nombre']  # Ordenar por nombre de forma ascendente
        verbose_name = "Categoría de Giro"
        verbose_name_plural = "Categorías de Giro"


class Giro(models.Model):
    codigo = models.CharField(max_length=10, unique=True)  # Código único para el giro
    nombre = models.CharField(max_length=100)  # Nombre del giro
    categoria = models.ForeignKey(CategoriaGiro, on_delete=models.CASCADE, null=False, default=0)

    def __str__(self):
        return f"{self.codigo} - {self.nombre}"
    
    class Meta:
        db_table = 'giro'  # Nombre de la tabla en la base de datos
        ordering = ['nombre']  # Ordenar por nombre de forma ascendente
        unique_together = ('codigo', 'nombre')  # Asegurar que la combinación de código y nombre sea única
        verbose_name = "Giro"
        verbose_name_plural = "Giros"
    
class Proveedor(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    rut = models.CharField(max_length=12, unique=True, default='00.000.000-0') 
    nombre = models.CharField(max_length=100)  # Campo para el nombre del proveedor
    direccion = models.TextField()              # Campo para la dirección del proveedor
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, related_name='proveedores')  # Relación con el modelo Comuna
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='proveedores')  # Relación con el modelo Region
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, related_name='proveedores')
    telefono = models.CharField(max_length=15)  # Campo para el teléfono del proveedor
    email = models.EmailField()                  # Campo para el correo electrónico del proveedor
    fecha_creacion = models.DateTimeField(auto_now_add=True)  # Fecha de creación del proveedor
    fecha_actualizacion = models.DateTimeField(auto_now=True)  # Fecha de la última actualización
    giro = models.ForeignKey(Giro, on_delete=models.SET_NULL, null=True)  # Relación con el modelo Giro
    logo = models.ImageField(upload_to='static/images/proveedores/logos/', blank=True, null=True)
    latitud = models.FloatField(null=True, blank=True, verbose_name="Latitud")
    longitud = models.FloatField(null=True, blank=True, verbose_name="Longitud")


    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Proveedor"
        verbose_name_plural = "Proveedores"
        db_table = "proveedor"

class Pedido(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, default=0)

    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completado', 'Completado'),
        ('Cancelado', 'Cancelado'),
        ('Devuelto', 'Devuelto'),
    ]
    
    proveedor = models.ForeignKey('Proveedor', on_delete=models.CASCADE, related_name="pedidos")
    fecha_creacion = models.DateTimeField(default=timezone.now)  
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente')
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    observaciones = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name="pedidos_creados", 
        null=True
    )
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        related_name="pedidos_actualizados", 
        null=True
    )

    def calcular_total(self):
        """
        Calcula el total del pedido basado en los DetallePedido asociados.
        """
        self.total = sum(
            detalle.subtotal for detalle in self.detalles.all()
        )
        self.save()

    def __str__(self):
        return f"Pedido {self.id} - {self.proveedor.nombre} - {self.estado}"

    class Meta:
        db_table = "pedido"
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
        ordering = ['-fecha_creacion']

class Detalle_Pedido(models.Model):
    direccion_entrega = models.ForeignKey(
        'Inventario.Bodega', 
        on_delete=models.CASCADE, 
        related_name="detalles",
        default=1
    )
    fecha_creacion = models.DateTimeField(default=timezone.now) 

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False, default=0)
    pedido = models.ForeignKey(
        Pedido, 
        on_delete=models.CASCADE, 
        related_name="detalles"
    )
    producto = models.ForeignKey(
        'Inventario.Producto', 
        on_delete=models.CASCADE, 
        related_name="detalles_pedido"
    )
    cantidad = models.PositiveIntegerField()
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.cantidad} x {self.producto.nombre} (Pedido {self.pedido.id})"

    class Meta:
        db_table = "detalle_pedido"
        verbose_name = "Detalle de Pedido"
        verbose_name_plural = "Detalles de Pedido"
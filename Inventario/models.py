from django.db import models
from Proveedor.models import *
from Ubicacion.models import Comuna, Region  # Asegúrate de importar las clases necesarias
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.core.exceptions import ValidationError

class Categoria(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(default=timezone.now) 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)





    def __str__(self):
        return f"{self.id} - {self.nombre}"

    class Meta:
        verbose_name = "Categoría"
        verbose_name_plural = "Categorías"
        db_table = "categoria"


class Bodega(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    nombre = models.CharField(max_length=100)  # Campo para el nombre de la bodega
    direccion = models.CharField(max_length=100)  # Campo para la dirección de la bodega
    capacidad = models.IntegerField(blank=False, null=False, default=0)
    cantidad_art = models.IntegerField(blank=True, null=True)  # Ahora puede ser nulo
    comuna = models.ForeignKey(Comuna, on_delete=models.SET_NULL, null=True, related_name='bodegas')  # Relación con el modelo Comuna
    provincia = models.ForeignKey(Provincia, on_delete=models.SET_NULL, null=True, related_name='bodegas')  # Relación con el modelo Provincia
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True, related_name='bodegas')  # Relación con el modelo Region
    fecha_creacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"
        db_table = "bodega"

    def calcular_cantidad_articulos(self):
        return self.cantidad_art if self.cantidad_art is not None else 0

    def clean(self):
        super().clean()
        if self.cantidad_art and self.capacidad:
            if self.cantidad_art > (self.capacidad + self.cantidad_art):
                raise ValidationError(
                    "La cantidad de artículos no puede exceder la capacidad total."
                )




class Producto(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)

    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, related_name='productos', default=0)
    sku = models.CharField(max_length=50, unique=True)  # Código único para cada producto
    nombre = models.CharField(max_length=100)
    proveedor = models.ForeignKey('Proveedor.Proveedor', on_delete=models.SET_NULL, null=True, related_name='productos')  # Usar cadena para evitar importación circular
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    precio_venta = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    porc_ganancias = models.DecimalField(max_digits=10, decimal_places=2)
    cantidad = models.IntegerField(blank=False, null=False, default=0)
    fecha_creacion = models.DateTimeField(default=timezone.now) 
    iva = models.DecimalField(max_digits=5, decimal_places=2, default=19.0)  # Agregar IVA como porcentaje por defecto (19%)
    bodega = models.ForeignKey('Bodega', on_delete=models.CASCADE)
    img = models.ImageField(blank=True, upload_to='static/images/productos/')

    def __str__(self):
            return f"{self.nombre} - {self.sku}"

    class Meta:
            verbose_name = "Producto"
            verbose_name_plural = "Productos"
            db_table = "producto"


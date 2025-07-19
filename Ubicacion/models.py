from django.db import models

# Ubicacion/models.py

class Region(models.Model):
    codigo_region = models.IntegerField(primary_key=True, unique=True)  # Cambiado a IntegerField
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Región"
        verbose_name_plural = "Regiones"
        db_table = "region"

class Provincia(models.Model):
    codigo_provincia = models.IntegerField(primary_key=True, unique=True)  # Cambiado a IntegerField
    nombre = models.CharField(max_length=100)
    region = models.ForeignKey(
        Region, 
        on_delete=models.CASCADE,
        related_name='provincias',
        to_field='codigo_region',  # Especificar que use codigo_region
        db_column='region_id'      # Nombre de la columna en la base de datos
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        db_table = "provincia"

class Comuna(models.Model):
    codigo_comuna = models.IntegerField(primary_key=True)  # Cambiado a IntegerField
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(
        Provincia,
        on_delete=models.CASCADE,
        related_name='comunas',
        to_field='codigo_provincia',  # Especificar que use codigo_provincia
        db_column='provincia_id'      # Nombre de la columna en la base de datos
    )

    def __str__(self):
        return self.nombre
    
    def get_region(self):
        return self.provincia.region

    class Meta:
        verbose_name = "Comuna"
        verbose_name_plural = "Comunas"
        db_table = "comuna"
        indexes = [
            models.Index(fields=['codigo_comuna']),
        ]
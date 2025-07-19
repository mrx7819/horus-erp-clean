from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    rut_empresa = models.CharField(max_length=20, blank=True, null=True, verbose_name="RUT Empresa")
    empresa = models.CharField(max_length=100, blank=True, null=True, verbose_name="Empresa")

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user_customuser'  # Define el nombre exacto de la tabla en la base de datos

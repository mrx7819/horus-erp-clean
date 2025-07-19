from django.db import models
from django.core.validators import RegexValidator, EmailValidator
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
from django.conf import settings
class Cliente(models.Model):
    rut = models.CharField(
        max_length=9,  # Ajusta el max_length si es necesario
        unique=True,
        validators=[RegexValidator(regex=r'^\d{7,8}[0-9Kk]$', message='El RUT debe contener entre 7 y 8 números seguidos de un dígito verificador (0-9 o K).')]
    )
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    direccion = models.CharField(max_length=200, blank=True, null=True)
    telefono = models.CharField(
        max_length=9,
        validators=[RegexValidator(regex=r'^\d{9}$', message='El teléfono debe tener 9 dígitos')]
    )
    email = models.EmailField(max_length=100, validators=[EmailValidator(message='Formato de email inválido')])
    fecha_nacimiento = models.DateField()
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True)
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    genero = models.CharField(max_length=10, choices=GENERO_CHOICES)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=False)
    
    def clean(self):
        # Validar que la fecha de nacimiento sea realista
        if self.fecha_nacimiento:
            today = datetime.date.today()
            age = today.year - self.fecha_nacimiento.year - ((today.month, today.day) < (self.fecha_nacimiento.month, self.fecha_nacimiento.day))
            if age > 100:
                raise ValidationError({'fecha_nacimiento': 'La edad no puede ser mayor a 100 años.'})

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rut}"
    
    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
        db_table = "cliente"
        ordering = ["-fecha_creacion"]
        unique_together = (("rut", "email"))
        indexes = [
            models.Index(fields=["rut", "email"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["rut", "email"], name="unique_rut_email")
        ]

class InteraccionCliente(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    TIPO_INTERACCION_CHOICES = [
        ('Llamada', 'Llamada'),
        ('Email', 'Email'),
        ('Reunión', 'Reunión'),
        ('Otro', 'Otro'),
    ]
    tipo_interaccion = models.CharField(max_length=100, choices=TIPO_INTERACCION_CHOICES)
    
    def __str__(self):
        return f"{self.cliente.nombre} {self.cliente.apellido} - {self.fecha}"
    
    class Meta:
        verbose_name = "Interacción del Cliente"
        verbose_name_plural = "Interacciones de Clientes"
        db_table = "interaccion_cliente"
        ordering = ["-fecha"]
        unique_together = (("cliente", "fecha"))
        indexes = [
            models.Index(fields=["cliente", "fecha"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["cliente", "fecha"], name="unique_cliente_fecha")
        ]
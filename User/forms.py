from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class RegistroForm(UserCreationForm):
    """
    Formulario de registro que incluye campos adicionales: RUT Empresa y Empresa.
    """
    rut_empresa = forms.CharField(
        max_length=20, 
        required=True, 
        help_text='Ingrese el RUT de su empresa'
    )
    empresa = forms.CharField(
        max_length=100, 
        required=True, 
        help_text='Ingrese el nombre de su empresa'
    )

    class Meta:
        model = CustomUser  # Usar el modelo personalizado
        fields = ['first_name', 'last_name', 'email', 'rut_empresa', 'empresa', 'password1', 'password2']

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email", 
        widget=forms.EmailInput(attrs={
            'placeholder': 'Ingrese su Email', 
            'class': 'custom-input'})  # Asegúrate de agregar la clase 'custom-input'
    )
    password = forms.CharField(
        label="Contraseña", 
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Ingrese su Contraseña', 
            'class': 'custom-input'})  # Asegúrate de agregar la clase 'custom-input'
    )

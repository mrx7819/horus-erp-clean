from rest_framework import serializers
from .models import Categoria, Bodega

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'  # Incluye todos los campos del modelo

class BodegaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bodega
        fields = '__all__'  # Incluye todos los campos del modelo

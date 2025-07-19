from rest_framework import serializers
from .models import Cliente, InteraccionCliente

class InteraccionClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteraccionCliente
        exclude = ['cliente']  # Excluir cliente para que no sea requerido en el JSON de entrada

class ClienteSerializer(serializers.ModelSerializer):
    interacciones = InteraccionClienteSerializer(many=True, write_only=True)

    class Meta:
        model = Cliente
        fields = [
            'rut', 'nombre', 'apellido', 'direccion', 'telefono', 'email',
            'fecha_nacimiento', 'genero', 'user', 'interacciones'
        ]

    def create(self, validated_data):
        # Extraer datos de interacciones
        interacciones_data = validated_data.pop('interacciones', [])
        # Crear cliente
        cliente = Cliente.objects.create(**validated_data)
        # Crear interacciones asociadas al cliente
        for interaccion_data in interacciones_data:
            InteraccionCliente.objects.create(cliente=cliente, **interaccion_data)
        return cliente

class ListaClienteSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        # Crear múltiples clientes y sus interacciones
        clientes = []
        for cliente_data in validated_data:
            interacciones_data = cliente_data.pop('interacciones', [])
            cliente = Cliente.objects.create(**cliente_data)
            for interaccion_data in interacciones_data:
                InteraccionCliente.objects.create(cliente=cliente, **interaccion_data)
            clientes.append(cliente)
        return clientes

class ClienteSerializer(serializers.ModelSerializer):
    interacciones = InteraccionClienteSerializer(many=True, write_only=True)

    class Meta:
        model = Cliente
        fields = [
            'rut', 'nombre', 'apellido', 'direccion', 'telefono', 'email',
            'fecha_nacimiento', 'genero', 'user', 'interacciones'
        ]
        list_serializer_class = ListaClienteSerializer  # Asigna el serializador de lista personalizado

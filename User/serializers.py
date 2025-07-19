from rest_framework import serializers
from .models import CustomUser

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser  # Cambiado a CustomUser
        fields = ['username', 'email', 'password', 'rut_empresa', 'empresa']

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            rut_empresa=validated_data.get('rut_empresa'),
            empresa=validated_data.get('empresa')
        )
        return user

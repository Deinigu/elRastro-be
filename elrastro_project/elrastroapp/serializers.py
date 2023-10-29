from rest_framework import serializers
from elrastroapp.models import Usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('correo', 'fotoURL', 'listaConver',
                   'productosVenta', 'reputacion', 'telefono', 
                   'vivienda', 'contrasenya', 'nombreUsuario')

from rest_framework import serializers
from elrastroapp.models import Usuario, Conversacion

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('correo', 'fotoURL', 'listaConver',
                   'productosVenta', 'reputacion', 'telefono', 
                   'vivienda', 'contrasenya', 'nombreUsuario')

class ConversacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversacion
        fields = ('__all__')
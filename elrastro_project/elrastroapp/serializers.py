from rest_framework import serializers
from elrastroapp.models import Usuario
from elrastroapp.models import Producto

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('correo', 'fotoURL', 'listaConver',
                   'productosVenta', 'reputacion', 'telefono', 
                   'vivienda', 'contrasenya', 'nombreUsuario')
class ProductoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Producto
        fields = '__all__'

from rest_framework import serializers
from elrastroapp.models import Usuario
from elrastroapp.models import Producto

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ('correo', 'fotoURL', 'listaConver',
                   'productosVenta', 'reputacion', 'telefono', 
                   'vivienda', 'contrasenya', 'nombreUsuario')
class ProductoSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length = 24)
    Nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    fecha = serializers.DateField(input_formats=["%d/%m/%Y"])
    fotoURL = serializers.CharField()
    precio = serializers.DecimalField(max_digits=6, decimal_places=2)
    tags = serializers.CharField(max_length = 200)
    ubicacion = serializers.CharField(max_length = 100)
    vendedor = serializers.CharField(max_length = 24)
    cierre = serializers.DateField(input_formats=["%d/%m/%Y"])
    pujas = serializers.ListField(child=serializers.CharField())

    

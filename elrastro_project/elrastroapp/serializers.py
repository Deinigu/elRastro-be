from rest_framework import serializers

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
    
class UsuarioSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length = 24)    
    correo = serializers.EmailField()
    fotoURL = serializers.URLField()
    listaConver = serializers.ListField(child=serializers.CharField())
    productosVenta = serializers.ListField(child=serializers.CharField())
    reputacion = serializers.FloatField()
    telefono = serializers.CharField()
    vivienda = serializers.CharField()
    contrasenya = serializers.CharField()
    nombreUsuario = serializers.CharField()

class PujaSerializer(serializers.Serializer):
    _id = serializers.CharField()
    pujador = serializers.CharField()
    valor = serializers.DecimalField(max_digits=6, decimal_places=2)
    fecha = serializers.DateField(input_formats=["%d/%m/%Y"])
    producto = serializers.CharField()

class ConversacionSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length = 24)
    remitente = serializers.CharField()
    destinatario = serializers.CharField()
    n_mensajes = serializers.IntegerField()
    ultimo_mensaje = serializers.CharField()


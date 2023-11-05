from rest_framework import serializers

class UsuarioSerializer(serializers.Serializer):
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

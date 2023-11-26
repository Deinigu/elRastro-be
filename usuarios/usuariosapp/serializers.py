from rest_framework import serializers

class ValoracionSerializer(serializers.Serializer):
    nombreUsuario = serializers.CharField(max_length=24)
    numero = serializers.IntegerField()
    descripcion = serializers.CharField()

class UsuarioSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=24)
    correo = serializers.EmailField()
    fotoURL = serializers.URLField()
    listaConver = serializers.ListField(child=serializers.CharField())
    productosVenta = serializers.ListField(child=serializers.CharField())
    reputacion = serializers.FloatField()
    valoraciones = ValoracionSerializer(many=True)
    telefono = serializers.CharField()
    vivienda = serializers.CharField()
    contrasenya = serializers.CharField()
    nombreUsuario = serializers.CharField()
from rest_framework import serializers

class UsuarioSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=24, required=False)
    correo = serializers.CharField()
    fotoURL = serializers.CharField()
    listaConver = serializers.ListField(child=serializers.CharField())
    productosVenta = serializers.ListField(child=serializers.CharField())
    reputacion = serializers.FloatField()
    telefono = serializers.CharField()
    vivienda = serializers.CharField()
    nombreUsuario = serializers.CharField()
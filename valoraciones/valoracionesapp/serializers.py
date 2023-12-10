from rest_framework import serializers

class ValoracionSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length=24, required=False)
    idUsuario = serializers.CharField(max_length=24)
    idValorado = serializers.CharField(max_length=24)
    idProducto = serializers.CharField(max_length=24)
    puntuacion = serializers.FloatField()
    comentario = serializers.CharField()
    fecha = serializers.DateTimeField(required=False)

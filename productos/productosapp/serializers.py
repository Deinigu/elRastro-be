from rest_framework import serializers

class ProductoSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length = 24, required=False)
    Nombre = serializers.CharField(max_length=100)
    descripcion = serializers.CharField()
    fecha = serializers.DateTimeField(required=False)
    fotoURL = serializers.ListField(child=serializers.CharField())
    precio = serializers.DecimalField(max_digits=6, decimal_places=2)
    tags = serializers.CharField(max_length = 200)
    vendedor = serializers.CharField(max_length = 24)
    cierre = serializers.DateTimeField()
    pujas = serializers.ListField(child=serializers.CharField(), required=False)

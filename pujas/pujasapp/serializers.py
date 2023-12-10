from rest_framework import serializers

class PujaSerializer(serializers.Serializer):
    _id = serializers.CharField(max_length = 24, required=False)
    pujador = serializers.CharField()
    valor = serializers.DecimalField(max_digits=6, decimal_places=2)
    fecha = serializers.DateTimeField(required=False)
    producto = serializers.CharField()

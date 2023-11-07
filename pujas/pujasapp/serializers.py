from rest_framework import serializers

class PujaSerializer(serializers.Serializer):
    _id = serializers.CharField()
    pujador = serializers.CharField()
    valor = serializers.DecimalField(max_digits=6, decimal_places=2)
    fecha = serializers.DateTimeField(input_formats=["%d/%m/%Y"])
    producto = serializers.CharField()

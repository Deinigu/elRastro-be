from rest_framework import serializers

class TokenSerializer(serializers.Serializer):
    idtoken = serializers.CharField()
from rest_framework import serializers

class ChatSerializer(serializers.Serializer):
    userId = serializers.CharField(required=True)
    texto = serializers.CharField(required=True)
    fecha = serializers.DateTimeField(required=True)

class ConversacionSerializer(serializers.Serializer):
    _id = serializers.CharField(required=False)
    usuario1 = serializers.CharField(required=True)
    usuario2 = serializers.CharField(required=True)
    productoId = serializers.CharField(required=True)
    chats = ChatSerializer(many=True, required=False)
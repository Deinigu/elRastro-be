from django.shortcuts import render


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from elrastroapp.models import Usuario, Conversacion
from elrastroapp.serializers import UsuarioSerializer, ConversacionSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = usuario_list()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse(usuarios_serializer.data, safe=False)    # 'safe=False' for objects serialization  
    
# Si vas a actualizar conversacion en la BBDD recuerda actualizar el models.py y el serializers.py

@api_view(['GET'])
def conversaciones_list_view(request):
    if request.method == 'GET':
        conversaciones = conversaciones_list()
        conversacion_serializer = ConversacionSerializer(conversaciones, many=True)
        return JsonResponse(conversacion_serializer.data, safe=False)

def usuario_list():
    usuarios = Usuario.objects.all()
    return usuarios

def conversaciones_list():
    conversaciones = Conversacion.objects.all()
    return conversaciones

def conversaciones_de(usuario):
    conversacionesResultado = Conversacion.objects.filter(remitente=usuario)
    return conversacionesResultado

def delete_conversacion(conversacion):
    Conversacion.delete(conversacion)
    conversacion.delete()

def update_conversacion(conversacion, conversacionNueva):
    conversacion.remitente = conversacionNueva.remitente
    conversacion.destinatario = conversacionNueva.destinatario
    conversacion.n_mensajes = conversacionNueva.n_mensajes
    conversacion.ultimo_mensaje = conversacionNueva.ultimo_mensaje
    conversacion.save()

def create_conversacion(remitente, destinatario, n_mensajes, ultimo_mensaje):
    conversacion = Conversacion(remitente=remitente, destinatario=destinatario, n_mensajes=n_mensajes, ultimo_mensaje=ultimo_mensaje)
    conversacion.save()
    return conversacion
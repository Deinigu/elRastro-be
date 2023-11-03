from django.shortcuts import render, get_object_or_404
import pymongo
from pymongo import ReturnDocument

from bson import ObjectId
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from elrastroapp.models import Usuario, Conversacion
from elrastroapp.serializers import UsuarioSerializer, ConversacionSerializer
from rest_framework.decorators import api_view

# Create your views here.

my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# First define the database name
dbname = my_client['ElRastro']

collection_conversaciones = dbname["conversaciones"]

@api_view(['GET', 'POST', 'DELETE'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = usuario_list()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse(usuarios_serializer.data, safe=False)    # 'safe=False' for objects serialization

#Detalles de una conversacion
@api_view(['GET'])
def conversacion_details_view(request, idConversacion):
    if request.method == 'GET':
        conversacion = collection_conversaciones.find_one(ObjectId(idConversacion))
        conversacion_serializer = ConversacionSerializer(conversacion, many=False)
        return JsonResponse(conversacion_serializer.data, safe=False)

#Lista de todas las conversaciones
@api_view(['GET'])
def conversaciones_list_view(request):
    if request.method == 'GET':
        conversaciones = collection_conversaciones.find({})
        conversacion_serializer = ConversacionSerializer(conversaciones, many=True)
        return JsonResponse(conversacion_serializer.data, safe=False)

#Eliminar una conversacion de la BBDD
@api_view(['DELETE'])
def conversacion_delete_view(request, idConversacion):
    if request.method == 'DELETE':
        delete_data = collection_conversaciones.delete_one({'_id': ObjectId(idConversacion)})
        if delete_data.deleted_count == 1:
            # Document was successfully deleted
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            # Document with the given ObjectId was not found
            return Response(status=status.HTTP_404_NOT_FOUND)

#Crear una conversación
@api_view(['POST'])
def conversacion_create_view(request):
    if request.method == 'POST':
        remitente = request.POST.get("remitente")
        destinatario = request.POST.get("destinatario")
        conversacion = {
            "_id": ObjectId(),
            "remitente": ObjectId(remitente),
            "destinatario": ObjectId(destinatario),
            "n_mensajes": 0,
            "ultimo_mensaje": ""
        }
        result = collection_conversaciones.insert_one(conversacion)
        if result.acknowledged:
            # Document was successfully created, return its ObjectId
            return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        else:
            # Failed to create the document
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Actualizar una conversación
@api_view(['POST'])
def conversacion_update_view(request, idConversacion):
    if request.method == 'POST':
        data = request.data
        remitente = data.get("remitente")
        destinatario = data.get("destinatario")
        n_mensajes = data.get("n_mensajes")
        ultimo_mensaje = data.get("ultimo_mensaje")
        result = collection_conversaciones.update_one(
            {'_id': ObjectId(idConversacion)},
            {'$set':{
                'remitente': ObjectId(remitente),
                'destinatario': ObjectId(destinatario),
                'n_mensajes': n_mensajes,
                'ultimo_mensaje': str(ultimo_mensaje)}
            }
        )
        if result.acknowledged:
            # Document was successfully created, return its ObjectId
            return Response({"message": "Document updated"}, status=status.HTTP_200_OK)
        else:
            # Failed to create the document
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def usuario_list():
    usuarios = Usuario.objects.all()
    return usuarios
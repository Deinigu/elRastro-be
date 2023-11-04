from django.shortcuts import render, get_object_or_404
import pymongo

from bson import ObjectId
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status

from elrastroapp.serializers import UsuarioSerializer, ConversacionSerializer
from rest_framework.decorators import api_view

# Create your views here.

my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# First define the database name
dbname = my_client['ElRastro']

collection_conversaciones = dbname["conversaciones"]

#Detalles de una conversacion
@api_view(['GET'])
def conversacion_details_view(request, idConversacion):
    if request.method == 'GET':
        conversacion = collection_conversaciones.find_one(ObjectId(idConversacion))
        conversacion['remitente'] = str(ObjectId(conversacion.get('remitente', [])))
        conversacion['destinatario'] = str(ObjectId(conversacion.get('destinatario', [])))
        conversacion_serializer = ConversacionSerializer(data=conversacion, many=False)
        if conversacion_serializer.is_valid():
            json_data = conversacion_serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(conversacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

#Lista de todas las conversaciones
@api_view(['GET'])
def conversaciones_list_view(request):
    if request.method == 'GET':
        conversaciones = list(collection_conversaciones.find({}))
        for conversacion in conversaciones:
            conversacion['remitente'] = str(ObjectId(conversacion.get('remitente', [])))
            conversacion['destinatario'] = str(ObjectId(conversacion.get('destinatario', [])))
        conversacion_serializer = ConversacionSerializer(data=conversaciones, many=True)
        if conversacion_serializer.is_valid():
            json_data = conversacion_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(conversacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Eliminar una conversacion de la BBDD
@api_view(['DELETE'])
def conversacion_delete_view(request, idConversacion):
    if request.method == 'DELETE':
        delete_data = collection_conversaciones.delete_one({'_id': ObjectId(idConversacion)})
        if delete_data.deleted_count == 1:
            return Response({"message": "Conversación eliminada con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

#Crear una conversación
@api_view(['POST'])
def conversacion_create_view(request):
    if request.method == 'POST':
        data = request.data
        remitente = data.get("remitente")
        destinatario = data.get("destinatario")
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
            return Response({"message": "Conversación creada con éxito"}, status=status.HTTP_201_CREATED)
        else:
            # Failed to create the document
            return Response({"error": "Conversación no creada"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#Actualizar una conversación
@api_view(['PUT'])
def conversacion_update_view(request, idConversacion):
    if request.method == 'PUT':
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
            return Response({"message": "Conversación actualizada"}, status=status.HTTP_200_OK)
        else:
            # Failed to create the document
            return Response({"error": "Conversación no encontrada"}, status=status.HTTP_404_NOT_FOUND)
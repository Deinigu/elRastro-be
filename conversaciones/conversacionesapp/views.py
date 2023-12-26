from django.shortcuts import render

from conversacionesapp.serializers import ConversacionSerializer
from conversacionesapp.serializers import ChatSerializer

import pymongo
import requests

from datetime import datetime

from bson import ObjectId
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import status

from pymongo import ReturnDocument

from django.shortcuts import render, get_object_or_404

# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------
# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro-TerceraEntrega']

# Colecciones
collection_conversaciones = dbname["conversaciones"]

# -------------------------------------  VISTA DE LAS CONVERSACIONES ----------------------------------------

# Lista todas las conversaciones
@api_view(['GET'])
def conversaciones_list(request):
    if request.method == 'GET':
        conversaciones = list(collection_conversaciones.find())
        for c in conversaciones:
            c['_id'] = str(c['_id'])
            c['usuario1'] = str(c['usuario1'])
            c['usuario2'] = str(c['usuario2'])
            c['productoId'] = str(c['productoId'])
        conversaciones_serializer = ConversacionSerializer(data=conversaciones, many=True)
        if conversaciones_serializer.is_valid():
            return Response(conversaciones_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(conversaciones_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Lista todas las conversaciones de un usuario
@api_view(['GET'])
def conversaciones_list_usuario(request, usuarioId):
    if request.method == 'GET':
        usuarioId = ObjectId(usuarioId)
        conversaciones = list(collection_conversaciones.find({'$or': [{'usuario1': usuarioId}, {'usuario2': usuarioId}]}))
        for c in conversaciones:
            c['_id'] = str(c['_id'])
            c['usuario1'] = str(c['usuario1'])
            c['usuario2'] = str(c['usuario2'])
            c['productoId'] = str(c['productoId'])
        conversaciones_serializer = ConversacionSerializer(data=conversaciones, many=True)
        if conversaciones_serializer.is_valid():
            return Response(conversaciones_serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(conversaciones_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtiene los detalles de una conversación
@api_view(['GET'])
def conversacion_detail(request, conversacionId):
    if request.method == 'GET':
        conversacion = collection_conversaciones.find_one({'_id': ObjectId(conversacionId)})
        if conversacion:
            conversacion['_id'] = str(conversacion['_id'])
            conversacion['usuario1'] = str(conversacion['usuario1'])
            conversacion['usuario2'] = str(conversacion['usuario2'])
            conversacion['productoId'] = str(conversacion['productoId'])
            conversaciones_serializer = ConversacionSerializer(data=conversacion)
            if conversaciones_serializer.is_valid():
                return Response(conversaciones_serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(conversaciones_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Conversacion no encontrada."}, status=status.HTTP_404_NOT_FOUND)

# Obtiene los mensajes de una conversación y agrega un nuevo mensaje
@api_view(['GET', 'POST'])
def chats_list_add(request, conversacionId):
    if request.method == 'GET':
        conversacion = collection_conversaciones.find_one({'_id': ObjectId(conversacionId)})
        if conversacion:
            chats = conversacion.get('chats', [])
            chats_serializer = ChatSerializer(data=chats, many=True)
            if chats_serializer.is_valid():
                json_data = chats_serializer.data
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                return Response(chats_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Conversacion no encontrada."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'POST':
        serializer = ChatSerializer(data=request.data)
        if serializer.is_valid():
            chat_data = serializer.validated_data
            chat_data['fecha'] = datetime.now()
            result = collection_conversaciones.update_one(
                {'_id': ObjectId(conversacionId)},
                {'$push': {'chats': chat_data}}
            )
            if result.acknowledged:
                return Response(chat_data, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Mensaje no creado."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtiene el ID de la conversación entre dos usuarios
@api_view(['GET'])
def conversacion_get(request, usuario1, usuario2):
    if request.method == 'GET':
        usuario1 = ObjectId(usuario1)
        usuario2 = ObjectId(usuario2)
        conversacion = collection_conversaciones.find_one({
            '$or': [{'usuario1': usuario1, 'usuario2': usuario2},
                    {'usuario1': usuario2, 'usuario2': usuario1}]
        })
        if conversacion:
            return Response(str(ObjectId(conversacion.get('_id', []))), status=status.HTTP_200_OK)
        else:
            return Response({"error": "Conversacion no encontrada."}, status=status.HTTP_404_NOT_FOUND)

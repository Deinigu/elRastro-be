from django.http import HttpRequest
from django.shortcuts import render

from valoracionesapp.serializers import ValoracionSerializer

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
from rest_framework.renderers import JSONRenderer

# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------
# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro-TerceraEntrega']

# Colecciones
collection_valoraciones = dbname["valoraciones"]

print(dbname.list_collection_names())

# Create your views here.

#Devuelve las valoraciones hechas de un usario en concreto
@api_view(['GET'])
def valoraciones_hechas(request, idUsuario):
    if request.method == 'GET':
        valoraciones = list(collection_valoraciones.find({"idUsuario": ObjectId(idUsuario)}))
        for valoracion in valoraciones:
            valoracion['_id'] = str(ObjectId(valoracion.get('_id',[])))
            valoracion['idUsuario'] = str(ObjectId(valoracion.get('idUsuario',[])))
            valoracion['idValorado'] = str(ObjectId(valoracion.get('idValorado',[])))
            valoracion['idProducto'] = str(ObjectId(valoracion.get('idProducto',[])))
        
        serializer = ValoracionSerializer(data=valoraciones, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

#Devuelve las valoraciones hacia un usario en concreto
@api_view(['GET'])
def valoraciones_recibidas(request, idUsuario):
    if request.method == 'GET':
        valoraciones = list(collection_valoraciones.find({"idValorado": ObjectId(idUsuario)}))
        for valoracion in valoraciones:
            valoracion['_id'] = str(ObjectId(valoracion.get('_id',[])))
            valoracion['idUsuario'] = str(ObjectId(valoracion.get('idUsuario',[])))
            valoracion['idValorado'] = str(ObjectId(valoracion.get('idValorado',[])))
            valoracion['idProducto'] = str(ObjectId(valoracion.get('idProducto',[])))
        
        serializer = ValoracionSerializer(data=valoraciones, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Crea una valoración
@api_view(['POST'])
def crear_valoracion(request):
    if request.method == 'POST':
        serializer = ValoracionSerializer(data=request.data)
        if serializer.is_valid():
            valoracion = serializer.validated_data
            valoracion['_id'] = ObjectId()
            valoracion['idUsuario'] = ObjectId(valoracion['idUsuario'])
            valoracion['idValorado'] = ObjectId(valoracion['idValorado'])
            valoracion['idProducto'] = ObjectId(valoracion['idProducto'])
            valoracion['fecha'] = datetime.now()
            result = collection_valoraciones.insert_one(valoracion)
            
            # Recacula la reputacion media del usuario
            http_request = HttpRequest()
            http_request.method = 'GET'
            http_request.user = request.user
            valorado = valoraciones_recibidas(http_request, valoracion['idValorado'])
            reputacion = 0
            for v in valorado.data:
                reputacion += v['puntuacion']
            if len(valorado.data) > 0:
                reputacion = reputacion / len(valorado.data)
            
            #Actualiza la reputacion del usuario
            perValorada = requests.get('http://localhost:8000/api/usuarios/' + str(valoracion['idValorado']) + '/')
            perValorada = perValorada.json()
            reputacion = round(reputacion, 2)
            perValorada['reputacion'] = reputacion
            res = requests.put('http://localhost:8000/api/usuarios/update/' + str(perValorada['_id']) + '/', json=perValorada)
            if result.acknowledged and res.status_code == status.HTTP_200_OK:
                return Response({"message": "Valoracion creada con éxito",},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Algo salió mal. Valoracion no creada."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        


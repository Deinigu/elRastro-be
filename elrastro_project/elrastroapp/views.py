from django.shortcuts import render

import pymongo
from pymongo import ReturnDocument

from datetime import datetime

from bson import ObjectId
from rest_framework.response import Response

from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from elrastroapp.models import Usuario, Producto
from elrastroapp.serializers import ProductoSerializer, UsuarioSerializer
from rest_framework.decorators import api_view

# Create your views here.

my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# First define the database name
dbname = my_client['ElRastro']

collection_productos = dbname["productos"]

@api_view(['GET', 'POST', 'DELETE'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = usuario_list()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse(usuarios_serializer.data, safe=False)    # 'safe=False' for objects serialization  

def usuario_list():
    usuarios = Usuario.objects.all()
    return usuarios

# Lista con todos los productos
@api_view(['GET'])
def productos_list_view(request):
    if request.method == 'GET':
        productos = collection_productos.find({})
        productos_serializer = ProductoSerializer(productos, many= True)
        return JsonResponse(productos_serializer.data, safe = False)
    
# Detalles de un producto
@api_view(['GET'])
def productos_detail_view(request, idProducto):
    if request.method == 'GET':
        producto = collection_productos.find_one(ObjectId(idProducto))
        producto_serializer = ProductoSerializer(producto, many = False) 
        return JsonResponse(producto_serializer.data, safe=False)

# Crear un producto
@api_view(['POST'])
def productos_create_view(request):
    if request.method == 'POST':
        now = datetime.now()
        fecha = now.strftime("%d/%m/%Y")
        
        data = request.data
                
        nombre = data.get("Nombre")
        descripcion = data.get("descripcion")
        fotoURL = data.get("fotoURL")
        precio = data.get("precio")
        tags = data.get("tags")
        ubicacion = data.get("ubicacion")
        vendedor = data.get("vendedor")
        cierre = data.get("cierre")
        
        producto = {
            "_id" : ObjectId(),
            "Nombre" : nombre,
            "descripcion" : descripcion,
            "fecha" : fecha,
            "fotoURL" : fotoURL,
            "precio" : precio,
            "tags" : tags,
            "ubicacion" : ubicacion,
            "vendedor" : ObjectId(vendedor),
            "cierre" : cierre,
            "pujas" : []
        }
        
        result = collection_productos.insert_one(producto)
        if result.acknowledged:
            # Document was successfully created, return its ObjectId
            return Response({"id": str(result.inserted_id)}, status=status.HTTP_201_CREATED)
        else:
            # Failed to create the document
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
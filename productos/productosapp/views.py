from productosapp.serializers import  ProductoSerializer

import pymongo
import requests
import json

from datetime import datetime
from dateutil import parser

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
dbname = my_client['ElRastro-SegundaEntrega']

# Colecciones
collection_productos = dbname["productos"]

# -------------------------------------  VISTAS DE PRODUCTO ----------------------------------------
# Lista con todos los productos
@api_view(['GET', 'POST'])
def productos_list_view(request):
    if request.method == 'GET':
        productos = list(collection_productos.find({}))
        
        for p in productos:
            p['_id'] = str(ObjectId(p.get('_id',[])))
            p['vendedor'] = str(ObjectId(p.get('vendedor',[])))
            p['pujas'] = [str(ObjectId(puja)) for puja in p.get('pujas',[])]
        
        productos_serializer = ProductoSerializer(data=productos, many= True)
        if productos_serializer.is_valid():
            json_data = productos_serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(productos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'POST':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.validated_data
            producto['_id'] = ObjectId()
            producto['fecha'] = datetime.now()
            producto['pujas'] = []
            producto['precio'] = float(producto['precio'])  # Convertir Decimal a float
            producto['vendedor'] = ObjectId(producto['vendedor'])

            result = collection_productos.insert_one(producto)
            if result.acknowledged:
                url = 'http://localhost:8000/api/usuarios/add_producto/' + str(producto['vendedor']) + '/' + str(producto['_id']) + '/'                
                response = requests.put(url)
                if response.status_code == 200:
                    return Response({"message": "Producto creado con éxito."}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Algo salió mal. Producto no creado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response({"error": "Algo salió mal. Producto no creado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

@api_view(['GET', 'DELETE', 'PUT'])
def producto_view(request, idProducto):
    if request.method == 'GET':
        producto = collection_productos.find_one(ObjectId(idProducto))
        
        # Transformar los objectid en strings
        producto['_id'] = str(ObjectId(producto.get('_id',[])))
        producto['vendedor'] = str(ObjectId(producto.get('vendedor',[])))
        producto['pujas'] = [str(ObjectId(puja)) for puja in producto.get('pujas',[])]

        producto_serializer = ProductoSerializer(data=producto, many = False) 
        if producto_serializer.is_valid():
            json_data = producto_serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        producto = collection_productos.find_one({'_id': ObjectId(idProducto)})
        if producto:
            result = collection_productos.delete_one({'_id': ObjectId(idProducto)})
            if result.deleted_count == 1:
                url = 'http://localhost:8000/api/usuarios/delete_producto/' + str(producto['vendedor']) + '/' + idProducto + '/'                
                response = requests.put(url)
                if response.status_code == 200:
                    return Response({"message": "Producto eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)
                else:
                    return Response({"error": "Algo salió mal. Producto no eliminado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        serializer = ProductoSerializer(data=request.data)
        if serializer.is_valid():
            producto = serializer.validated_data
            producto['_id'] = ObjectId(idProducto)
            producto['precio'] = float(producto['precio'])
            
            result = collection_productos.replace_one({'_id': ObjectId(idProducto)}, producto)
            if result.acknowledged:
                return Response({"message": "Producto actualizado con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Producto no actualizado."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Agrega una puja a un producto
@api_view(['PUT'])
def add_puja_view(request, idProducto, idPuja):
    if request.method == 'PUT':
        producto = collection_productos.find_one({'_id': ObjectId(idProducto)})
        if producto:
            producto['pujas'].append(idPuja)
            result = collection_productos.replace_one({'_id': ObjectId(idProducto)}, producto)
            if result.acknowledged:
                return Response({"message": "Puja añadida con éxito."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Puja no añadida."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)



# -------------------------------------  BÚSQUEDAS PARAMETRIZADAS ----------------------------------------

# Devuelve los productos de un determinado usuario y cuya fecha de cierre sea anterior a la actual
@api_view(['GET'])
def productos_usuario_anterior_view(request, idUsuario):
    if request.method == 'GET':
        productos = list(collection_productos.find({"vendedor": ObjectId(idUsuario), 
                                                    "cierre": {"$lt": datetime.now()}}))
        
        for p in productos:
            p['_id'] = str(ObjectId(p.get('_id',[])))
            p['vendedor'] = str(ObjectId(p.get('vendedor',[])))
            p['pujas'] = [str(ObjectId(puja)) for puja in p.get('pujas',[])]
        
        productos_serializer = ProductoSerializer(data=productos, many= True)
        if productos_serializer.is_valid():
            json_data = productos_serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(productos_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Buscar productos cuyo precio sea menor o igual de un número dado.
@api_view(['GET'])
def productos_menor_precio_view(request, precio):
    if request.method == 'GET':
        productos = list(collection_productos.find({'precio': {'$lte': float(precio)}}))
        for producto in productos:
            producto['_id'] = str(ObjectId(producto.get('_id',[])))
            producto['vendedor'] = str(ObjectId(producto.get('vendedor',[])))
            producto['pujas'] = [str(ObjectId(puja)) for puja in producto.get('pujas',[])]
        
        producto_serializer = ProductoSerializer(data=productos, many=True)
        if producto_serializer.is_valid():
            json_data = producto_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
#Buscar productos por una cadena de texto.
#Si no encuentra ningun producto al principio, busca por palabras sueltas de longitud 4 o más.
@api_view(['GET'])
def productos_busqueda_view(request, cadena):
    if request.method == 'GET':
        collection_productos.create_index([("Nombre", "text")], name="Nombre_text")
        productos = list(collection_productos.find({'$text': {'$search': cadena}}))
        if not productos:
            palabras = cadena.split()
            for palabra in palabras:
                if len(palabra) >= 4:
                    productos = list(collection_productos.find({'$text': {'$search': palabra}}))
                    if productos:
                        break
                    else:
                        for palabra in palabras:
                            productos = list(collection_productos.find({'tags': {'$elemMatch': {'$eq': palabra}}}))
                            if productos:
                                break
        for producto in productos:
            producto['_id'] = str(ObjectId(producto.get('_id',[])))
            producto['vendedor'] = str(ObjectId(producto.get('vendedor',[])))
            producto['pujas'] = [str(ObjectId(puja)) for puja in producto.get('pujas',[])]
        
        producto_serializer = ProductoSerializer(data=productos, many=True)
        if producto_serializer.is_valid():
            json_data = producto_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(producto_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

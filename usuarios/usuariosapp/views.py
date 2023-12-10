from django.shortcuts import render

from usuariosapp.serializers import UsuarioSerializer

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
dbname = my_client['ElRastro-SegundaEntrega']

# Colecciones
collection_usuarios = dbname["usuarios"]

print(dbname.list_collection_names())

# Create your views here.
# -------------------------------------  VISTAS DE USUARIOS ----------------------------------------

#Obtener la lista de usuarios y crear un usuario
@api_view(['GET', 'POST'])
def lista_usuarios_crear(request):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({}))
        for usuario in usuarios:
            usuario['_id'] = str(usuario.get('_id',[]))
            usuario['listaConver'] = [str(id) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(id) for id in usuario.get('productosVenta', [])]
            
        serializer = UsuarioSerializer(data=usuarios, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'POST':
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            usuario = serializer.validated_data
            existing_user = collection_usuarios.find_one({'correo': usuario['correo']})
            if existing_user is not None:
                return Response({"error": "Ya existe un usuario con ese correo."},
                                status=status.HTTP_400_BAD_REQUEST)
            usuario['_id'] = ObjectId()
            usuario['listaConver'] = []
            usuario['productosVenta'] = []
            usuario['reputacion'] = 0.0
            result = collection_usuarios.insert_one(usuario)
            if result.acknowledged:
                return Response({"message": "Usuario creado con éxito",},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Algo salió mal. Usuario no creado."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Obtener un usuario, borrar un usuario o actualizar un usuario
@api_view(['GET', 'DELETE', 'PUT'])
def view_usuario(request, usuario_id):
    usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
    if usuario:
        if request.method == 'GET':
            usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
            serializer = UsuarioSerializer(data=usuario)
            if serializer.is_valid():
                json_data = serializer.data
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        elif request.method == 'DELETE':
            result = collection_usuarios.delete_one({'_id': ObjectId(usuario_id)})
            if result.acknowledged:
                return Response({"message": "Usuario eliminado con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Usuario no eliminado."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        elif request.method == 'PUT':
            serializer = UsuarioSerializer(data=request.data)
            if serializer.is_valid():
                usuario = serializer.validated_data
                usuario['_id'] = ObjectId(usuario_id)
                result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
                if result.acknowledged:
                    return Response({"message": "Usuario actualizado con éxito",},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Algo salió mal. Usuario no actualizado."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    

# -------------------------------------  BÚSQUEDAS PARAMETRIZADAS ----------------------------------------

#Añadir un producto a la lista de productos en venta de un usuario
@api_view(['PUT'])
def add_producto_venta_view(request, usuario_id, producto_id):
    if request.method == 'PUT':
        usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            usuario['productosVenta'].append(producto_id)
            result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
            if result.acknowledged:
                return Response({"message": "Producto añadido a la lista de productos en venta con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Producto no añadido a la lista de productos en venta."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
        
#Eliminar un producto de la lista de productos en venta de un usuario
@api_view(['PUT'])
def delete_producto_venta_view(request, usuario_id, producto_id):
    if request.method == 'PUT':
        usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            usuario['productosVenta'].remove(producto_id)
            result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
            if result.acknowledged:
                return Response({"message": "Producto eliminado de la lista de productos en venta con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Producto no eliminado de la lista de productos en venta."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

#Añade una conversacion a la lista de conversaciones de un usuario
@api_view(['PUT'])
def add_conversacion(request, usuario_id, conversacion_id):
    if request.method == 'PUT':
        print(usuario_id)
        usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            usuario['listaConver'].append(conversacion_id)
            result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
            if result.acknowledged:
                return Response({"message": "Conversacion añadida a la lista de conversaciones con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Conversacion no añadida a la lista de conversaciones."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

#Eliminar una conversacion de la lista de conversaciones de un usuario
@api_view(['PUT'])
def delete_conversacion(request, usuario_id, conversacion_id):
    if request.method == 'PUT':
        usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            usuario['listaConver'].remove(conversacion_id)
            result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
            if result.acknowledged:
                return Response({"message": "Conversacion eliminada de la lista de conversaciones con éxito",},
                                status=status.HTTP_200_OK)
            else:
                return Response({"error": "Algo salió mal. Conversacion no eliminada de la lista de conversaciones."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


# Buscar usuarios cuya reputación sea mayor de un número dado.
@api_view(['GET'])
def usuarios_mayor_reputacion_view(request, reputacion):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({'reputacion': {'$gt': float(reputacion)}}))
        for usuario in usuarios:
            usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
        usuario_serializer = UsuarioSerializer(data=usuarios , many=True)
        if usuario_serializer.is_valid():
            json_data = usuario_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Buscar usuarios cuya reputación sea menor de un número dado.
@api_view(['GET'])
def usuarios_menor_reputacion_view(request, reputacion):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({'reputacion': {'$lt': float(reputacion)}}))
        for usuario in usuarios:
            usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
            serializer = UsuarioSerializer(data=usuario)
            if serializer.is_valid():
                json_data = serializer.data
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        usuario_serializer = UsuarioSerializer(data=usuarios, many=True)
        if usuario_serializer.is_valid():
            json_data = usuario_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


        
# Devuelve quiénes han sido compradores de cualquiera de los productos ofrecidos por un determinado usuario
@api_view(['GET'])
def compradores_usuario_view(request, usuario_id):
    compradores = []
    if request.method == 'GET':
        url = 'http://localhost:8001/api/productos/anteriores/' + usuario_id
        response = requests.get(url)
        if response.status_code == 200:
            productos = response.json()
            for producto in productos:
                url = 'http://localhost:8002/api/pujas/ultima_puja/producto/' + str(producto['_id'])
                response = requests.get(url)
                if response.status_code == 200:
                    puja = response.json()
                    if puja['pujador'] not in compradores:
                        compradores.append(ObjectId(puja['pujador']))
            usuarios = list(collection_usuarios.find({'_id': {'$in': compradores}}))
            for usuario in usuarios:
                usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
                usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
                usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
                serializer = UsuarioSerializer(data=usuario)
                if serializer.is_valid():
                    json_data = serializer.data
                    return Response(json_data, status=status.HTTP_200_OK)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            usuario_serializer = UsuarioSerializer(data=usuarios, many=True)
            if usuario_serializer.is_valid():
                json_data = usuario_serializer.data 
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Productos no encontrados"}, status=status.HTTP_404_NOT_FOUND)
    
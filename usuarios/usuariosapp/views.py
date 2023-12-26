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
dbname = my_client['ElRastro-TerceraEntrega']

# Colecciones
collection_usuarios = dbname["usuarios"]

# -------------------------------------  VISTAS DE USUARIOS ----------------------------------------


# ---------------------------------------  CRUD BÁSICO ----------------------------------------


# Lista de usuarios y creación de un usuario
@api_view(['GET', 'POST'])
def lista_usuarios_crear(request):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({}))
        for usuario in usuarios:
            usuario['_id'] = str(usuario.get('_id', []))
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
                return Response({"message": "Usuario creado con éxito"},
                                status=status.HTTP_201_CREATED)
            else:
                return Response({"error": "Algo salió mal. Usuario no creado."},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Obtener, borrar o actualizar un usuario
@api_view(['GET', 'DELETE', 'PUT'])
def view_usuario(request, usuario_id):
    usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
    if usuario:
        if request.method == 'GET':
            usuario['_id'] = str(ObjectId(usuario.get('_id', [])))
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
                return Response({"message": "Usuario eliminado con éxito"},
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
                    return Response({"message": "Usuario actualizado con éxito"},
                                    status=status.HTTP_200_OK)
                else:
                    return Response({"error": "Algo salió mal. Usuario no actualizado."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    

# ---------------------------------------  EXTRAS Y BÚSQUEDAS PARAMETRIZADAS ----------------------------------------

# Añadir o eliminar un producto de la lista de productos en venta de un usuario
@api_view(['PUT', 'DELETE'])
def productos_venta_usuario_view(request, usuario_id, producto_id):
    usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})

    if usuario:
        if request.method == 'PUT':
            usuario['productosVenta'].append(producto_id)
        elif request.method == 'DELETE':
            try:
                usuario['productosVenta'].remove(producto_id)
            except ValueError:
                return Response({"error": "El producto no se encontraba en la lista de productos en venta."},
                                status=status.HTTP_400_BAD_REQUEST)

        result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
        if result.acknowledged:
            message = "Producto añadido a la lista de productos en venta con éxito" if request.method == 'PUT' else \
                      "Producto eliminado de la lista de productos en venta con éxito"
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            error_message = "Algo salió mal. Producto no {} de la lista de productos en venta.".format(
                "añadido" if request.method == 'PUT' else "eliminado")
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Añadir o eliminar una conversación de la lista de conversaciones de un usuario
@api_view(['PUT', 'DELETE'])
def conversaciones_usuario_view(request, usuario_id, conversacion_id):
    usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})

    if usuario:
        if request.method == 'PUT':
            usuario['listaConver'].append(conversacion_id)
        elif request.method == 'DELETE':
            try:
                usuario['listaConver'].remove(conversacion_id)
            except ValueError:
                return Response({"error": "La conversación no se encontraba en la lista de conversaciones."},
                                status=status.HTTP_400_BAD_REQUEST)

        result = collection_usuarios.replace_one({'_id': ObjectId(usuario_id)}, usuario)
        if result.acknowledged:
            message = "Conversación añadida a la lista de conversaciones con éxito" if request.method == 'PUT' else \
                      "Conversación eliminada de la lista de conversaciones con éxito"
            return Response({"message": message}, status=status.HTTP_200_OK)
        else:
            error_message = "Algo salió mal. Conversación no {} de la lista de conversaciones.".format(
                "añadida" if request.method == 'PUT' else "eliminada")
            return Response({"error": error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    else:
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
# Usuarios con reputación mayor o menor que un número dado
@api_view(['GET'])
def usuarios_reputacion_view(request, operador, reputacion):
    operadores = {'mayor': '$gt', 'menor': '$lt'}

    if request.method == 'GET' and operador in operadores:
        condicion = {'reputacion': {operadores[operador]: float(reputacion)}}
        usuarios = list(collection_usuarios.find(condicion))

        for usuario in usuarios:
            usuario['_id'] = str(ObjectId(usuario.get('_id', [])))
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]

        serializer = UsuarioSerializer(data=usuarios, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Operador no válido o método HTTP no permitido."},
                        status=status.HTTP_400_BAD_REQUEST)

# Compradores de productos ofrecidos por un usuario
@api_view(['GET'])
def compradores_usuario_view(request, usuario_id):
    compradores = []

    if request.method == 'GET':
        url_productos = f'http://localhost:8001/api/productos/anteriores/{usuario_id}'
        response_productos = requests.get(url_productos)

        if response_productos.status_code == 200:
            productos = response_productos.json()

            for producto in productos:
                url_puja = f'http://localhost:8002/api/pujas/ultima_puja/producto/{str(producto["_id"])}'
                response_puja = requests.get(url_puja)

                if response_puja.status_code == 200:
                    puja = response_puja.json()

                    if puja['pujador'] not in compradores:
                        compradores.append(ObjectId(puja['pujador']))

            usuarios = list(collection_usuarios.find({'_id': {'$in': compradores}}))

            for usuario in usuarios:
                usuario['_id'] = str(ObjectId(usuario.get('_id', [])))
                usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
                usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]

            serializer = UsuarioSerializer(data=usuarios, many=True)
            if serializer.is_valid():
                json_data = serializer.data
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Productos no encontrados"}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({"error": "Método HTTP no permitido."}, status=status.HTTP_400_BAD_REQUEST)
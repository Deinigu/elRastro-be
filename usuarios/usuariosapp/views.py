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
dbname = my_client['ElRastro']

# Colecciones
collection_usuarios = dbname["usuarios"]

# Create your views here.
# -------------------------------------  VISTAS DE USUARIOS ----------------------------------------

# OBTENER LISTA DE USUARIOS 

@api_view(['GET'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({}))

        # Pasar los ObjectId a String antes de pasar el serializer
        for usuario in usuarios:
            usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]

        serializer = UsuarioSerializer(data=usuarios, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

          
@api_view(['GET', 'PUT', 'DELETE'])
def view_usuario(request, usuario_id=None):
    print(request.method)
    if request.method == 'GET':
        print("GETTT")
        if usuario_id:
            # READ USER 
            usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
            if usuario:
                usuario = transform_user_ids(usuario)
                usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
                serializer = UsuarioSerializer(data=usuario)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'PUT':
        if usuario_id:
            # UPDATE USER 
            data = request.data
            usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
            if usuario:
                for key, value in data.items():
                    usuario[key] = value
                collection_usuarios.save(usuario)
                return Response({"message": "Usuario actualizado con éxito"}, status=status.HTTP_200_OK)
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

    elif request.method == 'DELETE':
        print("DELETE")
        if usuario_id:
            # DELETE USER
            result = collection_usuarios.delete_one({'_id': ObjectId(usuario_id)})
            if result.deleted_count == 1:
                return Response({"message": "Usuario eliminado con éxito"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

def transform_user_ids(usuario):
    usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
    usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
    return usuario


# Crear un usuario
@api_view(['POST'])
def create_usuario_view(request):
    print("ENTRA")
    if request.method == 'POST':
        data = request.data

        nombreUsuario = data.get("nombreUsuario")
        correo = data.get("correo")
        fotoURL = data.get("fotoURL")
        reputacion = 0.0
        telefono = data.get("telefono")
        vivienda = data.get("vivienda")
        contrasenya = data.get("contrasenya")

        usuario = {
            "_id": ObjectId(),
            "nombreUsuario": nombreUsuario,
            "correo": correo,
            "fotoURL": fotoURL,
            "listaConver": [],
            "productosVenta": [],
            "reputacion": float(reputacion),
            "telefono": telefono,
            "vivienda": vivienda,
            "contrasenya": contrasenya
        }

        result = collection_usuarios.insert_one(usuario)
        if result.acknowledged:
            return Response({"message": "Usuario creado con éxito",},
                            status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Algo salió mal. Usuario no creado."},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
# -------------------------------------  BÚSQUEDAS PARAMETRIZADAS ----------------------------------------

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
            print(len(productos))
            for producto in productos:
                url = 'http://localhost:8002/api/pujas/ultima_puja/producto/' + str(producto['_id'])
                response = requests.get(url)
                if response.status_code == 200:
                    puja = response.json()
                    print(puja['pujador'])
                    if puja['pujador'] not in compradores:
                        print("HOLAAAA")
                        compradores.append(ObjectId(puja['pujador']))
            print(compradores)
            usuarios = list(collection_usuarios.find({'_id': {'$in': compradores}}))
            print(usuarios)
            for usuario in usuarios:
                usuario['_id'] = str(ObjectId(usuario.get('_id',[])))
                usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
                usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
            usuario_serializer = UsuarioSerializer(data=usuarios, many=True)
            if usuario_serializer.is_valid():
                json_data = usuario_serializer.data 
                return Response(json_data, status=status.HTTP_200_OK)
            else:
                return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "Productos no encontrados"}, status=status.HTTP_404_NOT_FOUND)
    
from django.shortcuts import render

from usuariosapp.serializers import UsuarioSerializer

import pymongo

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

          
          
# CRUD: READ, UPDATE Y DELETE     

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def view_usuario(request, usuario_id=None):
    if request.method == 'GET':
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
        if usuario_id:
            # DELETE USER
            result = collection_usuarios.delete_one({'_id': ObjectId(usuario_id)})
            if result.deleted_count == 1:
                return Response({"message": "Usuario eliminado con éxito"}, status=status.HTTP_204_NO_CONTENT)
            return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# CRUD: CREATE USER

@api_view(['POST'])
def create_usuario(request):
    if request.method == 'POST':
        data = request.data
        if 'correo' in data and 'nombreUsuario' in data:
            usuario = collection_usuarios.insert_one(data)
            return Response({"message": "Usuario creado con éxito", "usuario_id": str(usuario.inserted_id)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Correo y nombre de usuario son campos requeridos"}, status=status.HTTP_400_BAD_REQUEST)

def transform_user_ids(usuario):
    usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
    usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
    return usuario

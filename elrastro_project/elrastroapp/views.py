from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from bson import ObjectId

import pymongo
from pymongo import ReturnDocument

from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404
 
from elrastroapp.serializers import UsuarioSerializer


# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------

# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro']

# Colección de usuarios
collection_usuarios = dbname["usuarios"]


# -------------------------------------  VISTAS DE USUARIOS ----------------------------------------

# OBTENER LISTA DE USUARIOS 

@api_view(['GET'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({}))

        # Pasar los ObjectId a String antes de pasar el serializer
        for usuario in usuarios:
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]

        serializer = UsuarioSerializer(data=usuarios, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# (CREATE) CREAR UN NUEVO USUARIO

@api_view(['POST'])
def create_usuario(request):
    if request.method == 'POST':
        data = request.data
        
        if 'correo' in data and 'nombreUsuario' in data:
            usuario = collection_usuarios.insert_one(data)
            return Response({"message": "Usuario creado con éxito", "usuario_id": str(usuario.inserted_id)}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Correo y nombre de usuario son campos requeridos"}, status=status.HTTP_400_BAD_REQUEST)

# (READ) LEER UN USUARIO 

@api_view(['GET'])
def get_usuario(request, usuario_id):
    if request.method == 'GET':
        usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            # Pasar los ObjectId a String antes de pasar el serializer
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
            serializer = UsuarioSerializer(data=usuario)
            if serializer.is_valid():
                json_data = serializer.data
                return Response(json_data, status=status.HTTP_200_OK)
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# (UPDATE) ACTUALIZAR UN USUARIO 

@api_view(['PUT'])
def update_usuario(request, usuario_id):
    if request.method == 'PUT':
        data = request.data
        usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
        if usuario:
            # Actualizar los campos necesarios
            for key, value in data.items():
                usuario[key] = value
            collection_usuarios.save(usuario)
            return Response({"message": "Usuario actualizado con éxito"}, status=status.HTTP_200_OK)
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# (DELETE) ELIMINAR UN USUARIO

@api_view(['DELETE'])
def delete_usuario(request, usuario_id):
    if request.method == 'DELETE':
        result = collection_usuarios.delete_one({'_id': ObjectId(usuario_id)})
        if result.deleted_count == 1:
            return Response({"message": "Usuario eliminado con éxito"}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)


'''
@api_view(['GET', 'POST'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = Usuario.objects.all()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return Response(usuarios_serializer.data)
    elif request.method == 'POST':
        usuario_serializer = UsuarioSerializer(data=request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data, status=status.HTTP_201_CREATED)
        return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
'''

'''
@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail_view(request, correo):
    try:
        usuario = Usuario.objects.get(correo=correo)
    except Usuario.DoesNotExist:
        return Response({'message': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        usuario_serializer = UsuarioSerializer(usuario)
        return Response(usuario_serializer.data)

    elif request.method == 'PUT':
        usuario_serializer = UsuarioSerializer(usuario, data=request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return Response(usuario_serializer.data)
        return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        usuario.delete()
        return Response({'message': 'Usuario eliminado correctamente'}, status=status.HTTP_204_NO_CONTENT)
'''

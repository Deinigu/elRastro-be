from elrastroapp.serializers import UsuarioSerializer, ConversacionSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.parsers import JSONParser
from rest_framework import status
from bson import ObjectId

import pymongo
from pymongo import ReturnDocument

from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------

# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro']

# Colecciones
collection_usuarios = dbname["usuarios"]
collection_conversaciones = dbname["conversaciones"]

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
        
# CRUD: READ, UPDATE Y DELETE     

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def view_usuario(request, usuario_id=None):
    if request.method == 'GET':
        if usuario_id:
            # READ USER 
            usuario = collection_usuarios.find_one({'_id': ObjectId(usuario_id)})
            if usuario:
                usuario = transform_user_ids(usuario)
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

# -------------------------------------  VISTAS DE CONVERSACIONES ----------------------------------------
  
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
        
# -------------------------------------  BÚSQUEDAS PARAMETRIZADAS ----------------------------------------
# Buscar conversaciones de un usuario cuyo número de mensajes sea mayor o igual a un número pasado por parámetro.
@api_view(['GET'])
def conversaciones_usuario_mayor_mensajes_view(request, usuario_id, n_mensajes):
    if request.method == 'GET':
        conversaciones = list(collection_conversaciones.find({'remitente': ObjectId(usuario_id), 'n_mensajes': {'$gte': n_mensajes}}))
        for conversacion in conversaciones:
            conversacion['remitente'] = str(ObjectId(conversacion.get('remitente', [])))
            conversacion['destinatario'] = str(ObjectId(conversacion.get('destinatario', [])))
        conversacion_serializer = ConversacionSerializer(data=conversaciones, many=True)
        if conversacion_serializer.is_valid():
            json_data = conversacion_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(conversacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def conversaciones_usuario_view(request, usuario_id):
    if request.method == 'GET':
        conversaciones = list(collection_conversaciones.find({'remitente': ObjectId(usuario_id)}))
        for conversacion in conversaciones:
            conversacion['remitente'] = str(ObjectId(conversacion.get('remitente', [])))
            conversacion['destinatario'] = str(ObjectId(conversacion.get('destinatario', [])))
        conversacion_serializer = ConversacionSerializer(data=conversaciones, many=True)
        if conversacion_serializer.is_valid():
            json_data = conversacion_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(conversacion_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
# Buscar usuarios cuya reputación sea mayor de un número dado.
@api_view(['GET'])
def usuarios_mayor_reputacion_view(request, reputacion):
    if request.method == 'GET':
        usuarios = list(collection_usuarios.find({'reputacion': {'$gt': reputacion}}))
        for usuario in usuarios:
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
        print(reputacion)
        usuarios = list(collection_usuarios.find({'reputacion': {'$lt': reputacion}}))
        print(usuarios)
        for usuario in usuarios:
            usuario['listaConver'] = [str(ObjectId(id)) for id in usuario.get('listaConver', [])]
            usuario['productosVenta'] = [str(ObjectId(id)) for id in usuario.get('productosVenta', [])]
        
        usuario_serializer = UsuarioSerializer(data=usuarios, many=True)
        if usuario_serializer.is_valid():
            json_data = usuario_serializer.data 
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
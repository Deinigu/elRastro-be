from elrastroapp.serializers import UsuarioSerializer, ConversacionSerializer, ProductoSerializer

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
collection_conversaciones = dbname["conversaciones"]
collection_productos = dbname["productos"]

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

# -------------------------------------  VISTAS DE CONVERSACIONES ----------------------------------------
  
#Detalles de una conversacion
@api_view(['GET'])
def conversacion_details_view(request, idConversacion):
    if request.method == 'GET':
        conversacion = collection_conversaciones.find_one(ObjectId(idConversacion))
        conversacion['_id'] = str(ObjectId(conversacion.get('_id',[])))
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
            conversacion['_id'] = str(ObjectId(conversacion.get('_id',[])))
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

# -------------------------------------  VISTAS DE PRODUCTO ----------------------------------------
# Lista con todos los productos
@api_view(['GET'])
def productos_list_view(request):
    if request.method == 'GET':
        productos = list(collection_productos.find({}))
        
        # Transformar los objectid en strings
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
    
# Detalles de un producto
@api_view(['GET'])
def productos_detail_view(request, idProducto):
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
            "precio" : float(precio),
            "tags" : tags,
            "ubicacion" : ubicacion,
            "vendedor" : ObjectId(vendedor),
            "cierre" : cierre,
            "pujas" : []
        }
        
        result = collection_productos.insert_one(producto)
        if result.acknowledged:
            return Response({"message" : "Producto creado con éxito."}, status=status.HTTP_201_CREATED)
        else:
            return Response({"error": "Algo salió mal. Producto no creado."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# Borrar un producto
@api_view(['DELETE'])
def delete_producto_view(request, idProducto):
    if request.method == 'DELETE':
        result = collection_productos.delete_one({'_id': ObjectId(idProducto)})
        if result.deleted_count == 1:
            return Response({"message": "Producto eliminado con éxito."}, status=status.HTTP_204_NO_CONTENT)
        return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)

# Actualizar un producto
@api_view(['PUT'])
def update_producto_view(request, idProducto):
    if request.method == 'PUT':
        data = request.data
                
        nombre = data.get("Nombre")
        descripcion = data.get("descripcion")
        fotoURL = data.get("fotoURL")
        precio = data.get("precio")
        tags = data.get("tags")
        ubicacion = data.get("ubicacion")
        cierre = data.get("cierre")
        
        result = collection_productos.update_one(
            {'_id': ObjectId(idProducto)},
            {'$set':{
                "Nombre" : nombre,
                "descripcion" : descripcion,
                "fotoURL" : fotoURL,
                "precio" : precio,
                "tags" : tags,
                "ubicacion" : ubicacion,
                "cierre" : cierre,}
            })
        if result.acknowledged:
            return Response({"message": "Producto actualizado."}, status=status.HTTP_200_OK)
        else:
            # Failed to create the document
            return Response({"error": "Producto no encontrado."}, status=status.HTTP_404_NOT_FOUND)
             

from pujasapp.serializers import PujaSerializer
import pymongo
import requests
from datetime import datetime
from bson import ObjectId
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------
# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro-TerceraEntrega']

# Colecciones
collection_pujas = dbname["pujas"]

# -------------------------------------  VISTA DE LAS PUJAS ----------------------------------------


# LISTA TODAS LAS PUJAS y crea una puja y la agrega a la lista de pujas del producto
@api_view(['GET', 'POST'])
def pujas_list_view(request):
    if request.method == 'GET':
        pujas = list(collection_pujas.find({}))

        # Pasar los ObjectId a String antes de pasar el serializer
        for puja in pujas:
            puja['_id'] = str(ObjectId(puja.get('_id', [])))
            puja['pujador'] = str(ObjectId(puja.get('pujador', [])))
            puja['producto'] = str(ObjectId(puja.get('producto', [])))

        serializer = PujaSerializer(data=pujas, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'POST':
        serializer = PujaSerializer(data=request.data)
        if serializer.is_valid():
            puja = serializer.validated_data
            puja['_id'] = ObjectId()
            puja['fecha'] = datetime.now()
            puja['pujador'] = ObjectId(puja['pujador'])
            puja['producto'] = ObjectId(puja['producto'])
            puja['valor'] = float(puja['valor'])
            puja['pagado'] = False
            puja['tasa'] = float(puja['tasa'])
            
            result = collection_pujas.insert_one(puja)
            if result.acknowledged:
                url='https://13.38.223.212:8001/api/productos/add_puja/' + str(puja['producto']) + '/' + str(puja['_id']) + '/'
                response = requests.put(url)
                if response.status_code == 200:
                    return Response({"message": "Puja creada"}, status=status.HTTP_201_CREATED)
                else:
                    return Response({"ERROR": "No se ha agregado correctamente al producto"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"ERROR": "Puja no creada"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['GET', 'DELETE'])
def puja_detail_view(request, puja_id):
    if request.method == 'GET':
        if puja_id:
            # READ PUJA 
            puja = collection_pujas.find_one({'_id': ObjectId(puja_id)})
            if puja:
                puja['_id'] = str(ObjectId(puja.get('_id', [])))
                puja['pujador'] = str(ObjectId(puja.get('pujador', [])))
                puja['producto'] = str(ObjectId(puja.get('producto', [])))

                serializer = PujaSerializer(data=puja)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"ERROR": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)
    
    # Eliminar la puja - Método DELETE descomentado
    elif request.method == 'DELETE':
        delete_data = collection_pujas.delete_one({'_id': ObjectId(puja_id)})
        if delete_data.deleted_count == 1:
            return Response({"mensaje": "Puja eliminada con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)

# Actualiza una puja por su id pagado = true
@api_view(['PUT'])
def puja_pagada(request):
    print(request.data)
    if request.method == 'PUT':
        puja = collection_pujas.find_one({'_id': ObjectId(request.data.get('idPuja'))})
        if puja:
            puja['pagado'] = True
            result = collection_pujas.update_one({'_id': ObjectId(request.data.get('idPuja'))}, {'$set': puja})
            if result.acknowledged:
                return Response({"mensaje": "Puja pagada con éxito"}, status=status.HTTP_200_OK)
            else:
                return Response({"ERROR": "Puja no pagada"}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ERROR": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)

# Devuelve la última puja de un producto en concreto
@api_view(['GET'])
def ultima_puja_producto(request, producto_id):
    if request.method == 'GET':
        if producto_id:
            # READ PUJA 
            puja = collection_pujas.find_one({'producto': ObjectId(producto_id)},
                                              sort=[('fecha', -1)])
            if puja:
                puja['_id'] = str(ObjectId(puja.get('_id', [])))
                puja['pujador'] = str(ObjectId(puja.get('pujador', [])))
                puja['producto'] = str(ObjectId(puja.get('producto', [])))
                serializer = PujaSerializer(data=puja)
                if serializer.is_valid():
                    return Response(serializer.data, status=status.HTTP_200_OK)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response({"error": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Producto no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# Devuelve las pujas de un pujador en concreto.
@api_view(['GET'])
def pujas_usuario_view(request, usuario_id):
    if request.method == 'GET':
        pujas = list(collection_pujas.find({'pujador': ObjectId(usuario_id)}))
        for puja in pujas:
            puja['_id'] = str(ObjectId(puja.get('_id', [])))
            puja['pujador'] = str(ObjectId(puja.get('pujador', [])))
            puja['producto'] = str(ObjectId(puja.get('producto', [])))

        serializer = PujaSerializer(data=pujas, many=True)
        if serializer.is_valid():
            json_data = serializer.data
            return Response(json_data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# Devuelve la dirección de la persona pujadora
@api_view(['GET'])
def direccion_pujador(request, puja_id):
    if request.method == 'GET':
        if puja_id:
            puja = collection_pujas.find_one({'_id': ObjectId(puja_id)})
            if puja:
                pujador = puja.get('pujador')
                url = 'https://13.38.223.212:8000/api/usuarios/' + str(pujador) + '/'
                response = requests.get(url)
                if response.status_code == 200:
                    usuario = response.json()
                    if usuario:
                        direccion = usuario.get('vivienda')
                        return Response({"direccion": direccion}, status=status.HTTP_200_OK)
                    return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Puja no encontrada"}, status.HTTP_404_NOT_FOUND)
        return Response({"error": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)

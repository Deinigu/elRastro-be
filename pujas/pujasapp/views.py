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
dbname = my_client['ElRastro']

# Colecciones
collection_pujas = dbname["pujas"]

# -------------------------------------  VISTA DE LAS PUJAS ----------------------------------------

# LISTA TODAS LAS PUJAS
@api_view(['GET'])
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

# DETALLES PUJA
@api_view(['GET'])
def puja_detail_view(request, puja_id):
    if request.method == 'GET':
        if puja_id:
            # READ PUJA 
            puja = collection_pujas.find_one({'_id': ObjectId(puja_id)})
            puja['_id'] = str(ObjectId(puja.get('_id', [])))
            puja['pujador'] = str(ObjectId(puja.get('pujador', [])))
            puja['producto'] = str(ObjectId(puja.get('producto', [])))

            serializer = PujaSerializer(data=puja)
            if serializer.is_valid():
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ERROR": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)
      
# BORRAR PUJA
@api_view(['DELETE'])
def puja_delete_view(request, puja_id):
    if request.method == 'DELETE':
        delete_data = collection_pujas.delete_one({'_id': ObjectId(puja_id)})
        if delete_data.deleted_count == 1:
            return Response({"mensaje": "Puja eliminada con éxito"}, status=status.HTTP_200_OK)
        else:
            return Response({"ERROR": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        

# CREAR PUJA
@api_view(['POST'])
def puja_create_view(request):
    if request.method == 'POST':
        data = request.data
        pujador = data.get("pujador")
        producto = data.get("producto")
        valor = data.get("valor")
        fecha = datetime.now()
        puja = {
            "_id": ObjectId(),
            "pujador": ObjectId(pujador),
            "valor": float(valor),
            "fecha": fecha,
            "producto": ObjectId(producto)
        }
        result = collection_pujas.insert_one(puja)
        if result.acknowledged:
            # Document was successfully created, return its ObjectId
            return Response({"mensaje": "Puja creada con éxito"}, status=status.HTTP_201_CREATED)
        else:
            # Failed to create the document
            return Response({"ERROR": "Puja no creada"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
# UPDATE PUJA -- No tiene sentido poder actualizar una puja así que no hemos incluído esta función

'''@api_view(['PUT'])
def puja_update_view(request, puja_id):
    data = request.data
    pujador = data.get("pujador")
    producto = data.get("producto")
    valor = data.get("valor")
    fecha = datetime.now()
    result = collection_pujas.update_one(
        {'_id': ObjectId(puja_id)},
        {'$set':{
            "pujador": ObjectId(pujador),
            "valor": float(valor),
            "fecha": fecha,
            "producto": ObjectId(producto)}
        }
    )
    if result.acknowledged:
            # Document was successfully created, return its ObjectId
        return Response({"message": "Puja actualizada"}, status=status.HTTP_200_OK)
    else:
            # Failed to create the document
        return Response({"ERROR": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)

'''

#Devuelve la última puja de un producto en concreto
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
    
#Devuelve la dirección de la persona pujadora
@api_view(['GET'])
def direccion_pujador(request, puja_id):
    if request.method == 'GET':
        if puja_id:
            puja = collection_pujas.find_one({'_id': ObjectId(puja_id)})
            if puja:
                pujador = puja.get('pujador')
                url = 'http://localhost:8000/api/usuarios/' + str(pujador) + '/'
                response = requests.get(url)
                if response.status_code == 200:
                    usuario = response.json()
                    print("HOLA")
                    print(usuario)
                    if usuario:
                        direccion = usuario.get('vivienda')
                        return Response({"direccion": direccion}, status=status.HTTP_200_OK)
                    return Response({"error": "Usuario no encontrado"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"error": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"error": "Puja no encontrada"}, status=status.HTTP_404_NOT_FOUND)
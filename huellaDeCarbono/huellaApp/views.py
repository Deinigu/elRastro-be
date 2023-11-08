import pymongo

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from bson import ObjectId

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------
# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro']

# Colecciones
collection_usuarios = dbname["usuarios"]

# Devuelve la distancia entre dos puntos mediante sus direcciones postales
import math
@api_view(['GET'])
def huellaDeCarbono(request, idUsuario1, idUsuario2):
    if request.method == 'GET':
        usuario1 = collection_usuarios.find_one({'_id': ObjectId(idUsuario1)})
        usuario2 = collection_usuarios.find_one({'_id': ObjectId(idUsuario2)})

        direccion1 = usuario1['vivienda']
        direccion2 = usuario2['vivienda']

        # Crea una instancia del geocodificador de Nominatim
        geolocator = Nominatim(user_agent="my_geocoder")

        # Obtiene las coordenadas geográficas de la primera dirección postal
        ubicacion_1 = geolocator.geocode(direccion1)
        coordenadas_1 = (ubicacion_1.latitude, ubicacion_1.longitude)

        # Obtiene las coordenadas geográficas de la segunda dirección postal
        ubicacion_2 = geolocator.geocode(direccion2)
        coordenadas_2 = (ubicacion_2.latitude, ubicacion_2.longitude)

        # Calcula la distancia entre las dos ubicaciones
        distancia = geodesic(coordenadas_1, coordenadas_2).kilometers

        # Calcula la huella de carbono en funcion de la distancia
        huella_carbono = distancia * 0.142

        response_data = {
            'distancia': f"{round(distancia, 2)}",
            'huella_carbono': f"{round(huella_carbono, 2)}" ,
            'tasa_emisiones': f"{round(huella_carbono * 0.01, 2)}"
        }
        return JsonResponse(response_data, content_type='application/json', json_dumps_params={'ensure_ascii': False})
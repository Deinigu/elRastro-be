import pymongo

from bson import ObjectId

from django.http.response import JsonResponse
from rest_framework.decorators import api_view
from rest_framework import status

from geopy.geocoders import Nominatim

import requests

# ----------------------------------------  VISTAS DE LA APLICACIÓN ------------------------------
# Conexión a la base de datos MongoDB
my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro-TerceraEntrega']

# Colecciones
collection_usuarios = dbname["usuarios"]

@api_view(['GET'])
def obtener_hora_local(request, idUsuario):
    if request.method == 'GET':
        url1 = 'http://localhost:8000/api/usuarios/' + idUsuario + '/'
        response = requests.get(url1)
        if response.status_code != 200:
            return JsonResponse({'message': 'Error al obtener el usuario'}, status=status.HTTP_400_BAD_REQUEST)
        usuario = response.json()

        # Crea una instancia del geocodificador de Nominatim
        geolocator = Nominatim(user_agent="my_geocoder")

        # Obtiene las coordenadas geográficas de la primera dirección postal
        ubicacion = geolocator.geocode(usuario["vivienda"])

        # Realiza una solicitud a la API de Zona Horaria
        api_key = "DHM1KEXNQUTE"
        url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=position&lat={ubicacion.latitude}&lng={ubicacion.longitude}"
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            hora_local_persona1 = data["formatted"]
            return JsonResponse({
                "Hora_local": hora_local_persona1
            })

        return JsonResponse({"error": "No se pudo obtener la hora local"}, status=500)
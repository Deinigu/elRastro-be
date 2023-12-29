from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TokenSerializer

import pymongo
import requests

from google.oauth2 import id_token
from google.auth.transport import requests

from rest_framework.decorators import api_view
from rest_framework import status



my_client = pymongo.MongoClient('mongodb+srv://usuario:usuario@elrastrodb.oqjmaaw.mongodb.net/')

# Nombre de la base de datos
dbname = my_client['ElRastro-TerceraEntrega']

# Colecciones
collection_usuarios = dbname["usuarios"]

CLIENT_ID = '97897189905-91u0q02ni37ctgtgege5uidl9cefa6gt.apps.googleusercontent.com'

@api_view(['POST'])
def oauth(request):
    if request.method == 'POST':
        serializer = TokenSerializer(data=request.data)
        if serializer.is_valid():
            tokenData = serializer.validated_data
            try:
                token = tokenData['idtoken']
                idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
                userid = idinfo['sub']
                if userid:
                    return Response({"userid": userid,},
                                    status=status.HTTP_200_OK)
            except ValueError:
                # Invalid token
                
                return Response({"error": "Token no valido: "+token,},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

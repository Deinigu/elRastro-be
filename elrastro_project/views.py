from django.shortcuts import render


from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from elrastroapp.models import Usuario
from elrastroapp.serializers import UsuarioSerializer
from rest_framework.decorators import api_view

# Create your views here.

@api_view(['GET', 'POST', 'DELETE'])
def usuarios_list_view(request):
    if request.method == 'GET':
        usuarios = usuario_list()
        usuarios_serializer = UsuarioSerializer(usuarios, many=True)
        return JsonResponse(usuarios_serializer.data, safe=False)    # 'safe=False' for objects serialization  

def usuario_list():
    usuarios = Usuario.objects.all()
    return usuarios

@api_view(['GET', 'PUT', 'DELETE'])
def usuario_detail_view(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)
    except Usuario.DoesNotExist:
        return JsonResponse({'message': 'El usuario no existe'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        usuario_serializer = UsuarioSerializer(usuario)
        return JsonResponse(usuario_serializer.data)

    elif request.method == 'PUT':
        usuario_serializer = UsuarioSerializer(usuario, data=request.data)
        if usuario_serializer.is_valid():
            usuario_serializer.save()
            return JsonResponse(usuario_serializer.data)
        return JsonResponse(usuario_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        usuario.delete()
        return JsonResponse({'message': 'Usuario eliminado satisfactoriamente'}, status=status.HTTP_204_NO_CONTENT)

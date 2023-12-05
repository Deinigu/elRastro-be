from django.urls import path
from huellaApp import views

urlpatterns = [
    # USUARIOS
    path('api/huella/<str:idUsuario1>/<str:idUsuario2>/', views.huellaDeCarbono, name='huellaDeCarbono'),
    path('api/coordenadas/<str:idUsuario>/', views.getCoordenadas),
]
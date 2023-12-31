from django.urls import path
from valoracionesapp import views

urlpatterns = [
    path('api/valoracion/', views.crear_valoracion),
    path('api/valoraciones_hechas/<str:idUsuario>/', views.valoraciones_hechas),
    path('api/valoraciones_recibidas/<str:idUsuario>/', views.valoraciones_recibidas),   
]

from django.urls import path
from usuariosapp import views

urlpatterns = [
    # USUARIOS
    path('api/usuarios/', views.usuarios_list_view),
    path('api/usuarios/create/', views.create_usuario_view),
    path('api/usuarios/<str:usuario_id>/', views.view_usuario),
    path('api/usuarios/delete/<str:usuario_id>/', views.view_usuario),
    path('api/usuarios/update/<str:usuario_id>/', views.view_usuario),
    path('api/usuarios/mayor_reputacion/<str:reputacion>/', views.usuarios_mayor_reputacion_view),
    path('api/usuarios/menor_reputacion/<str:reputacion>/', views.usuarios_menor_reputacion_view),
    path('api/usuarios/compradores_de/<str:usuario_id>/', views.compradores_usuario_view),
]
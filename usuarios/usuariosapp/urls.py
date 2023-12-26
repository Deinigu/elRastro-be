from django.urls import path
from . import views

urlpatterns = [
    path('usuarios/', views.lista_usuarios_crear, name='lista_usuarios_crear'),
    path('usuarios/<str:usuario_id>/', views.view_usuario, name='view_usuario'),
    path('usuarios/<str:usuario_id>/productos/<str:producto_id>/', views.productos_venta_usuario_view, name='productos_venta_usuario_view'),
    path('usuarios/<str:usuario_id>/conversaciones/<str:conversacion_id>/', views.conversaciones_usuario_view, name='conversaciones_usuario_view'),
    path('usuarios/reputacion/<str:operador>/<str:reputacion>/', views.usuarios_reputacion_view, name='usuarios_reputacion_view'),
    path('usuarios/compradores/<str:usuario_id>/', views.compradores_usuario_view, name='compradores_usuario_view'),
]
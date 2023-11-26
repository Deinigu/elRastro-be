from django.urls import path
from usuariosapp import views

urlpatterns = [
    # USUARIOS
    path('api/usuarios/', views.lista_usuarios_crear),
    path('api/usuarios/create/', views.lista_usuarios_crear),
    path('api/usuarios/<str:usuario_id>/', views.view_usuario),
    path('api/usuarios/delete/<str:usuario_id>/', views.view_usuario),
    path('api/usuarios/update/<str:usuario_id>/', views.view_usuario),
    path('api/usuarios/mayor_reputacion/<str:reputacion>/', views.usuarios_mayor_reputacion_view),
    path('api/usuarios/menor_reputacion/<str:reputacion>/', views.usuarios_menor_reputacion_view),
    path('api/usuarios/compradores_de/<str:usuario_id>/', views.compradores_usuario_view),
    path('api/usuarios/add_producto/<str:usuario_id>/<str:producto_id>/', views.add_producto_venta_view),
    path('api/usuarios/add_conversacion/<str:usuario_id>/<str:conversacion_id>/', views.add_conversacion),
    path('api/usuarios/delete_producto/<str:usuario_id>/<str:producto_id>/', views.delete_producto_venta_view),
    path('api/usuarios/delete_conversacion/<str:usuario_id>/<str:conversacion_id>/', views.delete_conversacion),

]
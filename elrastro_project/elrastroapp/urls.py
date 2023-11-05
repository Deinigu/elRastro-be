from django.urls import path
from elrastroapp import views

urlpatterns = [

    # PUJAS
    path('api/pujas', views.pujas_list_view),
    path('api/puja_detail/<str:puja_id>', views.puja_detail_view),
    path('api/puja_create', views.puja_create_view),  
    path('api/puja_delete/<str:puja_id>', views.puja_delete_view),  
    path('api/puja_update/<str:puja_id>', views.puja_update_view) 

    # PRODUCTOS
    path('api/productos/', views.productos_list_view),
    path('api/productos/create/', views.productos_create_view),
    path('api/productos/update/<str:idProducto>/', views.update_producto_view),
    path('api/productos/delete/<str:idProducto>/', views.delete_producto_view),
    path('api/productos/<str:idProducto>/', views.productos_detail_view),
    
    # CONVERSACIONES
    path('api/conversaciones/', views.conversaciones_list_view),
    path('api/conversaciones/delete/<str:idConversacion>/', views.conversacion_delete_view),
    path('api/conversaciones/create/', views.conversacion_create_view),
    path('api/conversaciones/<str:idConversacion>/', views.conversacion_details_view),
    path('api/conversacion_update/<str:idConversacion>/', views.conversacion_update_view),
    
    # USUARIOS
    path('api/usuarios/', views.usuarios_list_view, name='usuarios_list'),
    path('api/usuarios/<str:usuario_id>/', views.view_usuario, name='view_usuario'),
    path('api/usuarios/create/', views.create_usuario, name='create_usuario')
    path('api/usuarios/create/', views.create_usuario, name='create_usuario'),
  
    # CONSULTAS
    path('api/conversaciones_usuario/<str:usuario_id>/', views.conversaciones_usuario_view, name='conversaciones_usuario'),
    path('api/conversaciones_usuario_mayor_mensajes/<str:usuario_id>/<int:n_mensajes>/', views.conversaciones_usuario_mayor_mensajes_view, name='conversaciones_usuario_mayor'),
    path('api/usuarios_mayor_reputacion/<int:reputacion>/', views.usuarios_mayor_reputacion_view, name='usuarios_mayor_reputacion'),
    path('api/usuarios_menor_reputacion/<int:reputacion>/', views.usuarios_menor_reputacion_view, name='usuarios_menor_reputacion'),


]
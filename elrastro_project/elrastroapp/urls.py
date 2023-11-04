from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/usuarios/', views.usuarios_list_view),
    path('api/productos/', views.productos_list_view),
    path('api/productos/create/', views.productos_create_view),
    path('api/productos/update/<str:idProducto>/', views.update_producto_view),
    path('api/productos/delete/<str:idProducto>/', views.delete_producto_view),
    path('api/productos/<str:idProducto>/', views.productos_detail_view),
    path('api/conversaciones/', views.conversaciones_list_view),
    path('api/conversacion_delete/<str:idConversacion>/', views.conversacion_delete_view),
    path('api/conversacion_details/<str:idConversacion>/', views.conversacion_details_view),
    path('api/conversacion_create/', views.conversacion_create_view),
    path('api/conversacion_update/<str:idConversacion>/', views.conversacion_update_view),
    path('api/usuarios/', views.usuarios_list_view, name='usuarios_list'),
    path('api/usuarios/<str:usuario_id>/', views.view_usuario, name='view_usuario'),
    path('api/usuarios/create/', views.create_usuario, name='create_usuario')
]
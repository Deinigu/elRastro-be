from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/conversaciones', views.conversaciones_list_view),
    path('api/conversacion_delete/<str:idConversacion>/', views.conversacion_delete_view),
    path('api/conversacion_details/<str:idConversacion>/', views.conversacion_details_view),
    path('api/conversacion_create/', views.conversacion_create_view),
    path('api/conversacion_update/<str:idConversacion>/', views.conversacion_update_view),
    path('api/usuarios/', views.usuarios_list_view, name='usuarios_list'),
    path('api/usuarios/<str:usuario_id>/', views.view_usuario, name='view_usuario'),
    path('api/usuarios/create/', views.create_usuario, name='create_usuario'),
    path('api/conversaciones_usuario/<str:usuario_id>/', views.conversaciones_usuario_view, name='conversaciones_usuario'),
    path('api/conversaciones_usuario_mayor_mensajes/<str:usuario_id>/<int:n_mensajes>/', views.conversaciones_usuario_mayor_mensajes_view, name='conversaciones_usuario_mayor'),
    path('api/usuarios_mayor_reputacion/<int:reputacion>/', views.usuarios_mayor_reputacion_view, name='usuarios_mayor_reputacion'),
    path('api/usuarios_menor_reputacion/<int:reputacion>/', views.usuarios_menor_reputacion_view, name='usuarios_menor_reputacion'),

]

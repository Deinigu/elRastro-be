from django.urls import path
from conversacionesapp import views

urlpatterns = [
    path('api/conversacion/create/', views.conversaciones_create),
    path('api/conversacion/<str:conversacionId>', views.conversacion_detail),
    path('api/conversacion/chats/<str:conversacionId>/', views.chats_list),
    path('api/conversacion/id/<str:usuario1>/<str:usuario2>/', views.conversacion_get),
    path('api/conversacion/add_chat/<str:conversacionId>/', views.chats_add),
    path('api/conversacion/usuario/<str:usuarioId>/', views.conversaciones_list),
]



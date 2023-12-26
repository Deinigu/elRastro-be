from django.urls import path
from conversacionesapp import views

urlpatterns = [
    path('api/conversaciones/', views.conversaciones_list),
    path('api/conversaciones/<str:usuarioId>/', views.conversaciones_list_usuario),
    path('api/conversacion/<str:conversacionId>/', views.conversacion_detail),
    path('api/conversacion/<str:conversacionId>/chat/', views.chats_list_add),
    path('api/conversacion/get/<str:usuario1>/<str:usuario2>/', views.conversacion_get),
]
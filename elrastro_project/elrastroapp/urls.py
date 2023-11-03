from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/usuarios', views.usuarios_list_view),
    path('api/conversaciones', views.conversaciones_list_view),
    path('api/conversaciones_delete/<str:idConversacion>/', views.conversacion_delete_view),
    path('api/conversacion_details/<str:idConversacion>/', views.conversacion_details_view),
    path('api/conversacion_create/', views.conversacion_create_view),
    path('api/conversacion_update/<str:idConversacion>/', views.conversacion_update_view),
]
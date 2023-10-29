from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/usuarios', views.usuarios_list_view),
    path('api/conversaciones', views.conversaciones_list_view),
    path('api/conversaciones/<str:usuario>/', views.conversaciones_de),
]
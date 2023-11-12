from django.urls import path
from horaLocalapp import views

urlpatterns = [
    # PRODUCTOS
    path('api/horaLocal/<str:idUsuario>/', views.obtener_hora_local),
]
    
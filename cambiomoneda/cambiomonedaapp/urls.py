from django.urls import path
from cambiomonedaapp import views

urlpatterns = [
    path('api/cambiomoneda/', views.cambio_moneda),
]
    
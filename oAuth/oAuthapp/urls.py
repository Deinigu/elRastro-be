from django.urls import path
from oAuthapp import views

urlpatterns = [
    path('logged', views.oauth)
    # otras rutas aquí...
]
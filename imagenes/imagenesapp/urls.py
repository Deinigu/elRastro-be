from django.urls import path
from imagenesapp import views

urlpatterns = [

    # PUJAS
    path('api/image/upload', views.upload_image),
]
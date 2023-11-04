from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/usuarios', views.usuarios_list_view),
    path('api/productos', views.productos_list_view),
    path('api/productos/<str:idProducto>', views.productos_detail_view),
    path('api/producto/create/', views.productos_create_view)
]
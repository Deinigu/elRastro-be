from django.urls import path
from productosapp import views

urlpatterns = [
    # PRODUCTOS
    path('api/productos/', views.productos_list_view),
    path('api/productos/create/', views.productos_list_view),
    path('api/productos/update/<str:idProducto>/', views.producto_view),
    path('api/productos/delete/<str:idProducto>/', views.producto_view),
    path('api/productos/<str:idProducto>/', views.producto_view),
    path('api/productos/anteriores/<str:idUsuario>/', views.productos_usuario_anterior_view),
    path('api/productos/precio_menor/<str:precio>/', views.productos_menor_precio_view),
    path('api/productos/add_puja/<str:idProducto>/<str:idPuja>/', views.add_puja_view),
]
    
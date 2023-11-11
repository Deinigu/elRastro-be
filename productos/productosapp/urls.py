from django.urls import path
from productosapp import views

urlpatterns = [
    # PRODUCTOS
    path('api/productos/', views.productos_list_view),
    path('api/productos/create/', views.productos_create_view),
    path('api/productos/update/<str:idProducto>/', views.update_producto_view),
    path('api/productos/delete/<str:idProducto>/', views.delete_producto_view),
    path('api/productos/<str:idProducto>/', views.productos_detail_view),
    path('api/productos/anteriores/<str:idUsuario>/', views.productos_usuario_anterior_view),
    path('api/productos/precio_menor/<str:precio>/', views.productos_menor_precio_view),
]
    
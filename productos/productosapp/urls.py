from django.urls import path
from productosapp import views

urlpatterns = [
    path('api/productos/', views.productos_list_view, name='productos-list'),
    path('api/productos/<str:idProducto>/', views.producto_detail_view, name='producto-detail'),
    path('api/productos/anteriores/<str:idUsuario>/', views.productos_usuario_anterior_view, name='productos-usuario-anterior'),
    path('api/productos/precio_menor/<str:precio>/', views.productos_menor_precio_view, name='productos-precio-menor'),
    path('api/productos/add_puja/<str:idProducto>/<str:idPuja>/', views.add_puja_to_producto_view, name='add-puja-to-producto'),
    path('api/productos/busqueda/<str:cadena>/', views.productos_busqueda_view, name='productos-busqueda'),
]
from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/usuarios/', views.usuarios_list_view),
    path('api/productos/', views.productos_list_view),
    path('api/productos/create/', views.productos_create_view),
    path('api/productos/update/<str:idProducto>/', views.update_producto_view),
    path('api/productos/delete/<str:idProducto>/', views.delete_producto_view),
    path('api/productos/<str:idProducto>/', views.productos_detail_view)

]
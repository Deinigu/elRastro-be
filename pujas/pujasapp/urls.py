from django.urls import path
from pujasapp import views

urlpatterns = [
    # PUJAS
    path('api/pujas/', views.pujas_list_view),
    path('api/pujas/create/', views.pujas_list_view),  
    path('api/pujas/<str:puja_id>/', views.puja_detail_view),
    #path('api/pujas/delete/<str:puja_id>/', views.puja_delete_view),  
    #path('api/puja_update/<str:puja_id>', views.puja_update_view),
    path('api/pujas/ultima_puja/producto/<str:producto_id>/', views.ultima_puja_producto),
    path('api/pujas/usuario/<str:usuario_id>/', views.pujas_usuario_view),
    path('api/pujas/direccion_pujador/<str:puja_id>/', views.direccion_pujador),

]
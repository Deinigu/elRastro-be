from django.urls import path
from pujasapp import views

urlpatterns = [
    # PUJAS
    path('api/pujas/', views.pujas_list_view),
    path('api/pujas/create/', views.puja_create_view),  
    path('api/pujas/<str:puja_id>/', views.puja_detail_view),
    path('api/pujas/delete/<str:puja_id>/', views.puja_delete_view),  
    #path('api/puja_update/<str:puja_id>', views.puja_update_view), 

]
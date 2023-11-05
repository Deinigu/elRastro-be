from django.urls import path
from elrastroapp import views

urlpatterns = [
    path('api/pujas', views.pujas_list_view),
    path('api/puja_detail/<str:puja_id>', views.puja_detail_view),
    path('api/puja_create', views.puja_create_view),  
    path('api/puja_delete/<str:puja_id>', views.puja_delete_view),  
    path('api/puja_update/<str:puja_id>', views.puja_update_view) 
]
from django.urls import path

from dashboard.views import DashboardHomeView, ProductDashboardView, AddProductsView, UpdateProductsView, update_status_in,update_status,CreateFormsView, OrderListView, ListModelsView, delete_model,OrderDetailView


app_name = 'dashboard'
 
urlpatterns = [
    path('', DashboardHomeView.as_view(), name='home'),
    path('products/', ProductDashboardView.as_view(), name='products'),
    path('add-products/', AddProductsView.as_view(), name='addprod'),
    path('product/<slug>', UpdateProductsView.as_view(), name='updateproduct'),
    path('create-utils', CreateFormsView.as_view(), name='utils_dash'),
    path('view-utils', ListModelsView.as_view(), name='utils_view'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='ord_details'),
    path('delete/<str:model>/<int:id>/', delete_model, name='delete_model'),
     path('orders/', OrderListView.as_view(), name='order_list'),
     path('update-status/<str:status>/<int:id>/', update_status, name='upt_stat'),
     path('update-status-in/<str:status>/<int:id>/', update_status_in, name='upt_stat_in'),
] 

 
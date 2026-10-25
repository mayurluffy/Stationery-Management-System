
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.add_product, name='add_product'),
    path('products/edit/<int:pk>/', views.edit_product,
         name='edit_product'),
    path('products/delete/<int:pk>/', views.delete_product,
         name='delete_product'),
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.add_order, name='add_order'),
]

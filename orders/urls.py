from django.urls import path
from . import views

urlpatterns = [
    path('add/', views.add_order, name='add-order'),
    path('<int:pk>/', views.get_order, name='order-detail'),
    path('my_orders/', views.get_my_orders, name='my-orders'),
]
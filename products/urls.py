from . import views
from django.urls import path

urlpatterns = [
    path('', views.list_products, name='product-list'),
    path('categories/', views.list_categories, name='categories-list'),
    path('categories/<int:pk>/', views.get_category, name='single-category'),
    path('<int:pk>/', views.get_product, name='single-product'),
    path('<int:pk>/comment/', views.comment_on_product, name='comment-on-product'),
    path('<int:pk>/all_reviews/', views.get_product_reviews, name='product-reviews'),
]
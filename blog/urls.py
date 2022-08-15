from django.urls import path
from . import views

urlpatterns = [
    path('posts/', views.list_blog_posts, name='blog-post-list'),
]
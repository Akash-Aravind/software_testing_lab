from django.urls import path
from . import views

urlpatterns = [
    path('home/', views.home, name='home'),
    path('products/', views.products, name='products'),
    path('cart/', views.cart, name='cart'),
    path('product-details/', views.product_details, name='product-details'),
]

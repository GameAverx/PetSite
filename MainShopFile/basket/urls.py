from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/update/<int:cart_item_id>/', views.update_cart_quantity, name='update_cart'),
    path('/delete/<int:cart_id>/', views.delete_cart_item, name='delete_cart_item'),
    path('/delete_cart', views.delete_cart, name='delete_cart'),
    path('/promocode', views.promocode, name='promocode'),
]
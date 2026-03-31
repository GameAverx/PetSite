from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/profile_edit', views.profile_edit, name='profile_edit'),
    path('/address_add', views.address_add, name='address_add'),
]
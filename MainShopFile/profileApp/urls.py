from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('/profile_edit', views.profile_edit, name='profile_edit'),
    path('/address_add', views.address_add, name='address_add'),
    path('/address_edit', views.address_edit, name='address_edit'),
    path('/address_update', views.address_update, name='address_update'),
]
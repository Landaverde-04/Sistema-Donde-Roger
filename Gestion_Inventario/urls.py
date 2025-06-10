from django.urls import path
from . import views

urlpatterns = [
    path('crear_inventario', views.crear_inventario, name='crear_inventario'),
    path('ver_inventario', views.ver_inventario, name='ver_inventario'),
]
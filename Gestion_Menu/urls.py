from django.urls import path
from . import views

urlpatterns = [
    path('registrar_producto_menu', views.registrar_producto_menu, name='registrar_producto_menu'),
]
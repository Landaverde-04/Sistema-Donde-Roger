from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
    path('deshabilitar/<int:id>/', views.deshabilitar_cliente, name='deshabilitar_cliente'),
]
from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
    path('listar_clientes/', views.listar_clientes, name='listar_clientes'),
    path('deshabilitar/<int:id>/', views.deshabilitar_cliente, name='deshabilitar_cliente'),
    path('listar_clientes_deshabilitados/', views.listar_clientes_deshabilitados, name='listar_clientes_deshabilitados'),
    path('habilitar/<int:id>/', views.habilitar_cliente, name='habilitar_cliente'),    
]
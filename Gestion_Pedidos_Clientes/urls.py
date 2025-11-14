from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('crear_pedido', views.crear_pedido, name='crear_pedido'),
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('pedidosHoy/', views.listar_pedidos, name='listar_pedidos'),
]
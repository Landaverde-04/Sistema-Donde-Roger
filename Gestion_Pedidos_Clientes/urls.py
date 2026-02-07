from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('crear_pedido', views.crear_pedido, name='crear_pedido'),
    re_path(r"^ver_pedido(?:/(?P<idPedido>.+))?$", views.ver_pedido, name='ver_pedido'),#Para ver un producto al menu
    re_path(r"^actualizar_estado_pedido(?:/(?P<idPedido>.+))?$", views.actualizar_estado_pedido, name='actualizar_estado_pedido'),#Para ver un producto al menu
    re_path(r"^pdf_pedido(?:/(?P<idPedido>.+))?$", views.generar_pdf_pedido, name='pdf_pedido'),
    path('api/clientes/', views.api_clientes, name='api_clientes'),
    path('api/clientes/direcciones/', views.api_direcciones, name='api_clientes'),
    path('pedidosHoy/', views.listar_pedidos_hoy, name='listar_pedidos_hoy'),
    path('historial/', views.listar_pedidos, name='listar_pedidos'),
]
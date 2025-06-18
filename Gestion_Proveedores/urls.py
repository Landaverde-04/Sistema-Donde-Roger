from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_proveedor/', views.registrar_proveedor, name='registrar_proveedor'),
    path('listar_proveedores/', views.listar_proveedor, name='listar_proveedores'),
    path('deshabilitar/<int:id>/', views.deshabilitar_proveedor, name='deshabilitar_proveedor'),
    path('proveedor_detalle/<int:id_proveedor>/', views.detalle_proveedor, name='detalle_proveedor'),
    path('editar_proveedor/<int:id>/', views.editar_proveedor, name='editar_proveedor'),
]
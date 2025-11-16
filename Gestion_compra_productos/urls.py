from django.urls import path
from . import views

urlpatterns = [
    path('crear_solicitud_compra/', views.crear_solicitud_compra, name='crear_solicitud_compra'),
    path('obtener_productos/<int:id_proveedor>/', views.obtener_productos, name='obtener_productos'),
    path('crear_solicitud_compra/guardar_pdf/', views.guardar_y_generar_pdf, name='guardar_y_generar_pdf'),
    path('preview_solicitud/', views.preview_solicitud_compra, name='preview_solicitud_compra'),
    path('listar_solicitudes_compra/', views.listar_solicitudes_compra, name='listar_solicitudes_compra'),
    path('ver_solicitud_compra_pdf/<int:pedido_id>/', views.ver_solicitud_compra_pdf, name='ver_solicitud_compra_pdf'),
]

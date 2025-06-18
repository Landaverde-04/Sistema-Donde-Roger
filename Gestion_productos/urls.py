from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_producto/', views.registrar_producto, name='registrar_producto'),
    path('listar_productos/', views.listar_productos, name='listar_productos'),
    path('actualizar_producto/<int:producto_id>/', views.actualizar_producto, name='actualizar_producto'),
    path('eliminar_producto/<int:producto_id>/', views.eliminar_producto, name='eliminar_producto'),
    path("detalle_producto/<int:producto_id>/", views.detalle_producto, name="detalle_producto"),
    path('deshabilitar_producto/<int:id>/', views.deshabilitar_producto, name='deshabilitar_producto'),
]
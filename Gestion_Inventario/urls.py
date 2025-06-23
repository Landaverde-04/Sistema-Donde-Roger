from django.urls import path
from . import views

urlpatterns = [
    path('', views.ver_inventario, name='ver_inventario'),
    path('crear_inventario', views.crear_inventario, name='crear_inventario'),
    path('ver_inventario', views.ver_inventario, name='ver_inventario'),
    path('ver_inventario/<int:inventarioId>/', views.ver_inventario, name='ver_inventario_id'),
    path('ver_detalle_inventario/<int:inventarioId>/<int:productoId>/', views.ver_detalle_inventario, name='ver_detalle_inventario'),
    #path('editar_detalle_inventario', views., name='crear_detalle_inventario'),
    path('listar_inventario', views.listar_inventario, name='listar_inventario'),
    path('crear_detalle_inventario', views.crear_detalle_inventario, name='crear_detalle_inventario'),
    path('api/productos/', views.api_productos, name='api_productos'),
    

]
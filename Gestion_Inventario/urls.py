from django.urls import path
from . import views

urlpatterns = [
    path('crear_inventario', views.crear_inventario, name='crear_inventario'),
    path('ver_inventario', views.ver_inventario, name='ver_inventario'),
    path('crear_detalle_inventario', views.crar_detalle_inventario, name='crear_detalle_inventario'),
    path('api/productos/', views.api_productos, name='api_productos'),

]
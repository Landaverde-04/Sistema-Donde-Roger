from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('registrar_producto_menu', views.registrar_producto_menu, name='registrar_producto_menu'), #Para registrar un producto al menu
    path('editar_producto_menu', views.editar_producto_menu , name='editar_producto_menu_id'), #la vista por defecto, no retorna nada pero se agrega para manejar la ruta
    path('editar_producto_menu/<int:productoMenuId>', views.editar_producto_menu, name='editar_producto_menu'),#La vista para editar un producto en especifico
    path('editar_producto_menu/<path:invalid>',views.editar_producto_menu , name='editar_producto_menu_default'),#Url para manejar rutas invalidas
    re_path(r"^ver_producto_menu(?:/(?P<productoMenuId>.+))?$", views.ver_producto_menu, name='ver_producto_menu'),#Para ver un producto al menu
    re_path(r"^cambiar_estado_producto_menu(?:/(?P<productoMenuId>.+))?$", views.cambiar_estado_producto_menu, name='cambiar_estado_producto_menu'),#Para ver un producto al menu
    path('menu', views.listar_productos_menu, name='listar_productos_menu'),
    path('deshabilitados', views.listar_productos_deshabilitados_menu, name='listar_productos_deshabilitados_menu'),
    path('api/productos/', views.api_producto_menu, name='api_producto_menu'),
    path('api/categorias/', views.api_categorias_producto_menu, name='api_categorias_producto_menu'),
]
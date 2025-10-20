from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('registrar_producto_menu', views.registrar_producto_menu, name='registrar_producto_menu'),
    path('editar_producto_menu', views.editar_producto_menu , name='editar_producto_menu_id'),
    path('editar_producto_menu/<int:productoMenuId>', views.editar_producto_menu, name='editar_producto_menu'),
    path('editar_producto_menu/<path:invalid>',views.editar_producto_menu , name='editar_producto_menu_default'),
]
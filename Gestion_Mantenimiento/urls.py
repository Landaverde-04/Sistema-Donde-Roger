# Gestion_Mantenimiento/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_mantenimiento, name='lista_mantenimiento'),
    path('registrar/', views.registrar_mantenimiento, name='registrar_mantenimiento'),
    path('<int:idMantenimiento>/', views.ver_mantenimiento, name='ver_mantenimiento'),
    path('<int:idMantenimiento>/modificar/', views.modificar_mantenimiento, name='modificar_mantenimiento'),
    path('<int:idMantenimiento>/eliminar/', views.eliminar_mantenimiento, name='eliminar_mantenimiento'),
]

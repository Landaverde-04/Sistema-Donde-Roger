from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_maquinaria, name='lista_maquinaria'),
    path('registrar/', views.registrar_maquinaria, name='registrar_maquinaria'),
    path('<int:idMaquinaria>/ver/', views.ver_maquinaria, name='ver_maquinaria'),
    path('<int:idMaquinaria>/modificar/', views.modificar_maquinaria, name='modificar_maquinaria'),
    path('<int:idMaquinaria>/eliminar/', views.eliminar_maquinaria, name='eliminar_maquinaria'),
]

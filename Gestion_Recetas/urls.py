from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_receta/', views.registrar_receta, name='registrar_receta'),
    path('listar_recetas/', views.listar_recetas, name='listar_recetas'),
    path('editar_receta/<int:idReceta>/', views.editar_receta, name='editar_receta'),
    path('detalle_receta/<int:idReceta>/', views.detalle_receta, name='detalle_receta'),
    path('deshabilitar_receta/<int:idReceta>/', views.deshabilitar_receta, name='deshabilitar_receta'),
    path('listar_recetas_deshabilitadas/', views.listar_recetas_deshabilitadas, name='listar_recetas_deshabilitadas'),
    path('habilitar_receta/<int:idReceta>/', views.habilitar_receta, name='habilitar_receta'),
]   
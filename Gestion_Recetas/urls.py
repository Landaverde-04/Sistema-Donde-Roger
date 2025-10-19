from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_receta/', views.registrar_receta, name='registrar_receta'),
    path('listar_recetas/', views.listar_recetas, name='listar_recetas'),
]   
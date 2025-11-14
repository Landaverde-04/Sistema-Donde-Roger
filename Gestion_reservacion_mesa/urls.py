from django.urls import path
from . import views

urlpatterns = [
    path('crear_reserva/', views.crear_reserva, name='crear_reserva'),
    path('ver_reservas/', views.ver_reservas, name='ver_reservas'),
    path('cancelar_reserva/', views.cancelar_reserva, name='cancelar_reserva'),
]

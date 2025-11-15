# reservas_mesa/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('nueva/', views.crear_reserva_mesa, name='crear_reserva_mesa'),
    path('hoy/', views.listar_reservas_hoy, name='listar_reservas_hoy'),
    path('mapa/', views.mapa_mesas, name='mapa_mesas'), 
    path('mesa/<int:mesa_id>/', views.detalle_mesa, name='detalle_mesa'),  
    path('<int:pk>/', views.ver_reserva_mesa, name='ver_reserva_mesa'),
    path('<int:pk>/cancelar/', views.cancelar_reserva_mesa, name='cancelar_reserva_mesa'),
    path('<int:pk>/eliminar/', views.eliminar_reserva_mesa, name='eliminar_reserva_mesa'),
    path('historial/', views.historial_reservas_mesa, name='historial_reservas_mesa'),
]

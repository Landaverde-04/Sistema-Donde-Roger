from django.urls import path
from . import views


urlpatterns = [
    path('', views.marcar_asistencia, name='marcar_asistencia'),
    path('registrar_empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('empleado_lista/', views.empleado_lista, name='empleado_lista'),
    path('ver/<str:idEmpleado>/', views.ver_empleado, name='ver_empleado'),
    path('modificar/<str:idEmpleado>/', views.modificar_empleado, name='modificar_empleado'),
    path('eliminar_empleado/<str:idEmpleado>/', views.eliminar_empleado, name='eliminar_empleado'),
    path('marcar_asistencia/', views.marcar_asistencia, name='marcar_asistencia'),
    path('historial_asistencia/', views.historial_asistencia, name='historial_asistencia'),
]




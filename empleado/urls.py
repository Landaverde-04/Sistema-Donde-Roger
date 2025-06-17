from django.urls import path
from . import views


urlpatterns = [
    path('registrar_empleado/', views.registrar_empleado, name='registrar_empleado'),
    path('empleado_lista/', views.empleado_lista, name='empleado_lista'),
    path('modificar/<str:idEmpleado>/', views.modificar_empleado, name='modificar_empleado'),
    path('eliminar/<str:idEmpleado>/', views.eliminar_empleado, name='eliminar_empleado'),
]




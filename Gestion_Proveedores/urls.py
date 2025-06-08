from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_proveedor/', views.registrar_proveedor, name='registrar_proveedor'),    
]
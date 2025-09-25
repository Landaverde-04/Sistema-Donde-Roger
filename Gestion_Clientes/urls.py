from django.urls import path, include
from . import views

urlpatterns = [
    path('registrar_cliente/', views.registrar_cliente, name='registrar_cliente'),
]
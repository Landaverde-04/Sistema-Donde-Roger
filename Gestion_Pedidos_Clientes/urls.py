from django.urls import path, re_path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('crear_pedido', views.crear_pedido, name='crear_pedido'),
]
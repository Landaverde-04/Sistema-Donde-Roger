from django.urls import path
from . import views
from .views import crear_usuario_view
from Gestion_Inventario import views as views_inventario 


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views_inventario.ver_inventario, name='home'),
    path('crear_usuario/', crear_usuario_view, name='crear_usuario'),
    path('usuario_lista/', views.usuario_lista_view, name='usuario_lista'),  
    path('ver_usuario/<int:usuario_id>/', views.ver_usuario_view, name='ver_usuario'), 
    path('modificar_usuario/<int:usuario_id>/', views.modificar_usuario_view, name='modificar_usuario'),
    path('eliminar_usuario/<int:usuario_id>/', views.eliminar_usuario_view, name='eliminar_usuario'),
]



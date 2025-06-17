from django.urls import path
from . import views
from .views import crear_usuario_view


urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.dashboard_view, name='dashboard'),
     path('crear_usuario/', crear_usuario_view, name='crear_usuario'),
]



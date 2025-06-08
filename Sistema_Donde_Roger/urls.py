"""
URL configuration for Sistema_Donde_Roger project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from Gestion_Proveedores.views import registrar_proveedor
from Gestion_productos.views import registrar_producto

urlpatterns = [
    path('admin/', admin.site.urls),
    path('registrar_proveedor/', registrar_proveedor, name='registrar_proveedor'),
    path('Productos/', include('Gestion_productos.urls')),    
    path('', include('seguridad.urls')),
]

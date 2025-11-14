
from django.contrib import admin
from django.urls import path, include
from Gestion_Proveedores.views import registrar_proveedor
from Gestion_productos.views import registrar_producto
from empleado.views import registrar_empleado
from django.conf import settings
from django.conf.urls.static import static
from Gestion_compra_productos.views import crear_solicitud_compra

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('Proveedor/', include('Gestion_Proveedores.urls')),
    path('',include('empleado.urls')),
    path('Producto/', include('Gestion_productos.urls')), 
    path('inventario/', include('Gestion_Inventario.urls')),
    path('empleado/', include('empleado.urls',)),
    path('seguridad/', include('seguridad.urls',)),
    path("maquinaria/", include("Gestion_Maquinaria.urls")),
    path('mantenimientos/', include('Gestion_Mantenimiento.urls')),
    path('clientes/', include('Gestion_Clientes.urls')),
    path('Menu/', include('Gestion_Menu.urls')),    
    path('recetas/', include('Gestion_Recetas.urls')),    
    path('crear_solicitud_compra/', include('Gestion_compra_productos.urls')),
    path('reservacion_mesa/', include('Gestion_reservacion_mesa.urls')),
    path('pedidos/', include('Gestion_Pedidos_Clientes.urls')),
        
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




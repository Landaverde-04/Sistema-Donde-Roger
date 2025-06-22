
from django.contrib import admin
from django.urls import path, include
from Gestion_Proveedores.views import registrar_proveedor
from Gestion_productos.views import registrar_producto
from empleado.views import registrar_empleado
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),    
    path('Proveedor/', include('Gestion_Proveedores.urls')),
    path('',include('Gestion_Inventario.urls')),
    path('Producto/', include('Gestion_productos.urls')), 
    path('inventario/', include('Gestion_Inventario.urls')),
    path('empleado/', include('empleado.urls',)),
    path('seguridad/', include('seguridad.urls',)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




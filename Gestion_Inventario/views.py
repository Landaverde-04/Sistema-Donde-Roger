from django.shortcuts import render, redirect
import datetime
from . import models

def ver_inventario(request):
    ultimo_inventario = models.Inventario.objects.all().last()
    if ultimo_inventario is None:
        return redirect('crear_inventario')
    else:
        fechaInventario = ultimo_inventario.fechaInventario
        horaInventario = ultimo_inventario.horaInventario
        return render(request, 'ver-inventario.html', {'fecha_inventario': fechaInventario, 'hora_inventario': horaInventario})
    
    
def crear_inventario(request):
    ultimo_inventario = models.Inventario.objects.all().last()
    if ultimo_inventario is None or ultimo_inventario.sePuedeEditar == False:
        current_date = datetime.datetime.now()
        fechaInventario = current_date.strftime('%Y-%m-%d')
        horaInventario = current_date.strftime('%H:%M:%S')
        inventario = models.Inventario.objects.create(idUsuario="si", fechaInventario=fechaInventario, horaInventario=horaInventario)
        inventario.save()
    elif ultimo_inventario.sePuedeEditar == True:
        fechaInventario = ultimo_inventario.fechaInventario
        horaInventario = ultimo_inventario.horaInventario

    return render(request, 'crear_inventario.html', {'fecha_inventario': fechaInventario, 'hora_inventario': horaInventario})

def crar_detalle_inventario(request):
    inventario_activo = models.Inventario.objects.filter(sePuedeEditar=True).first()
    # if inventario_activo:
    
        
     


    
# Create your views here.

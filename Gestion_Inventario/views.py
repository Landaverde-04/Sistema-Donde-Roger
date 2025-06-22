from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import datetime
from . import models
from Gestion_productos import models as models_productos

def api_productos(request):
    productos = list(models_productos.Producto.objects.all().order_by('nombreProducto').values())
    return JsonResponse(productos, safe=False)

def ver_inventario(request): #Funcion que renderiza el invetario actual
    ultimo_inventario = models.Inventario.objects.all().last()
    if ultimo_inventario is None:
        return redirect('crear_inventario')
    else:
        fechaInventario = ultimo_inventario.fechaInventario
        horaInventario = ultimo_inventario.horaInventario
        return render(request, 'ver-inventario.html', {'fecha_inventario': fechaInventario, 'hora_inventario': horaInventario})
    
    
@login_required
def crear_inventario(request): # Funcion que renderiza la pantalla de creacion de inventario
    ultimo_inventario = models.Inventario.objects.all().last()
    if ultimo_inventario is None or ultimo_inventario.sePuedeEditar == False:
        current_date = datetime.datetime.now()
        fechaInventario = current_date.strftime('%Y-%m-%d')
        horaInventario = current_date.strftime('%H:%M:%S')
        inventario = models.Inventario.objects.create(idUsuario=request.user, fechaInventario=fechaInventario, horaInventario=horaInventario, sePuedeEditar=True)
        inventario.save()
    elif ultimo_inventario.sePuedeEditar == True:
        fechaInventario = ultimo_inventario.fechaInventario
        horaInventario = ultimo_inventario.horaInventario

    return render(request, 'crear_inventario.html', {'fecha_inventario': fechaInventario, 'hora_inventario': horaInventario})

@login_required
def crar_detalle_inventario(request): #Funcion que renderiza la pantalla de creacion de inventario
    inventario_activo = models.Inventario.objects.filter(sePuedeEditar=True).first() #obtener el inventario activo en proceso
    if inventario_activo is None:
        return redirect('ver_inventario')
    else:
        if request.method == 'POST':
            print(request.POST)
            indices_keys = [key for key in request.POST.keys() if key.startswith('cantidad-')]
            for i in range(len(indices_keys)):
                detalle = models.DetalleInventario();
                detalle.idInventario = inventario_activo
                detalle.idProducto_id = request.POST['product']
                detalle.cantidadProducto = request.POST['cantidad-' + str(i+1)]
                detalle.fechaIngreso = request.POST['ingreso-' + str(i+1)][0:10].format('YYYY-MM-DD')
                detalle.horaIngreso = request.POST['ingreso-'+ str(i+1)][11:16].format('HH:MM:SS')
                detalle.fechaCaducidad = request.POST['caducidad-'+ str(i+1)].format('YYYY-MM-DD')
                detalle.save()
                print(detalle)
            return redirect('crear_inventario')
        elif request.method == 'GET':
            fecha_inventario = inventario_activo.fechaInventario
            hora_inventario = inventario_activo.horaInventario
            return render(request, 'crear_detalle_inventario.html', {'fecha_inventario': fecha_inventario, 'hora_inventario': hora_inventario})
    # if inventario_activo:
    

        
     


    
# Create your views here.

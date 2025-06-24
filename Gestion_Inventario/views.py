from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
import datetime
from . import models
from Gestion_productos import models as models_productos
from seguridad.decoradores import groups_required
from django.core.paginator import Paginator


#API para consultar los productos, inicialemente trae todos los productos, pero se modifico para traer solo
#los que no cuentan con un detalle de inventario para el inventario actual.
def api_productos(request):
    inventario_activo = models.Inventario.objects.filter(sePuedeEditar=True).first() #obtener el inventario activo en proceso
    
    productos_en_inventario = models.DetalleInventario.objects.filter(
        idInventario=inventario_activo
    ).values_list('idProducto__idProducto', flat=True)

    # Excluir esos productos del listado general
    productos = list(models_productos.Producto.objects.exclude(
        idProducto__in=productos_en_inventario
    ).order_by('nombreProducto').values())
    
    return JsonResponse(productos, safe=False)

##FUNCION PARA CREAR LA SUMATORIA DE STOCK PARA LOS DETALLES DE INVENTARIO: guarda en un diccionario
#con clave id y luego una lista para los atributos de nombre y cantidad sumadas
def resumir_inventario(QuerySet):
    if QuerySet is not None:
        resumen = {}
        for detalle in QuerySet:
            id = detalle.idProducto.idProducto
            if id not in resumen:
                resumen.update({id: [detalle.idProducto.nombreProducto, detalle.cantidadProducto]})
            elif id in resumen:
                resumen[id][1] += detalle.cantidadProducto
        print(resumen)
        return resumen
    
@login_required
def ver_inventario(request, inventarioId=None): #Funcion que renderiza el invetario solicitado, de no tener parametro renderiza el actual
    if inventarioId is not None:
        try:
            inventario = models.Inventario.objects.get(idInventario=inventarioId)
            if inventario is not None:
                detallesInventario = models.DetalleInventario.objects.filter(idInventario=inventario)
                resumenDetalles = resumir_inventario(detallesInventario)
                return render(request, 'ver_inventario.html', {'detalles':resumenDetalles, 'inventario': inventario})
        except:
            return redirect('ver_inventario')
    else:    
        ultimo_inventario = models.Inventario.objects.all().last()
        if ultimo_inventario is None:
            return redirect('crear_inventario')
        else:
            detallesInventario = models.DetalleInventario.objects.filter(idInventario=ultimo_inventario)
            resumenDetalles = resumir_inventario(detallesInventario)
            print(resumenDetalles)
            return render(request, 'ver_inventario.html', {'detalles':resumenDetalles,'inventario':ultimo_inventario})
    
    
@login_required
def crear_inventario(request): # Funcion que renderiza la pantalla de creacion de inventario
    if request.method == 'POST':
        print (request.POST)
        ultimo_inventario = models.Inventario.objects.all().last()
        ultimo_inventario.sePuedeEditar = False
        ultimo_inventario.save()
        return redirect('ver_inventario')
    
    resumenDetalles = {}
    ultimo_inventario = models.Inventario.objects.all().last()
    if ultimo_inventario is not None:
        detallesInventario = models.DetalleInventario.objects.filter(idInventario=ultimo_inventario)
        resumenDetalles = resumir_inventario(detallesInventario)
        if ultimo_inventario.sePuedeEditar == False:
            current_date = datetime.datetime.now()
            fechaInventario = current_date
            horaInventario = current_date
            inventario = models.Inventario.objects.create(idUsuario=request.user, fechaInventario=fechaInventario, horaInventario=horaInventario, sePuedeEditar=True)
            for detalle in detallesInventario:
                detalle_copia = models.DetalleInventario()
                detalle_copia.idProducto = detalle.idProducto
                detalle_copia.cantidadProducto = detalle.cantidadProducto
                detalle_copia.fechaIngreso = detalle.fechaIngreso
                detalle_copia.horaIngreso = detalle.horaIngreso
                detalle_copia.fechaCaducidad = detalle.fechaCaducidad
                detalle_copia.idInventario = inventario
                detalle_copia.save()
            inventario.save()
        elif ultimo_inventario.sePuedeEditar == True:
            inventario = ultimo_inventario
    elif ultimo_inventario is None:
            current_date = datetime.datetime.now()
            fechaInventario = current_date.strftime('%Y-%m-%d')
            horaInventario = current_date.strftime('%H:%M:%S')
            inventario = models.Inventario.objects.create(idUsuario=request.user, fechaInventario=fechaInventario, horaInventario=horaInventario, sePuedeEditar=True)
            inventario.save()
                

    return render(request, 'crear_inventario.html', {'inventario':inventario, 'detalles':resumenDetalles})


#Funcion que renderiza la pantalla de creacion de inventario: busca el inventario activo en proceso, de no encontrarlo
#redirige a la pantalla de ver inventario, si lo encuentra, muestra la pantalla de creacion de inventario.
@login_required
def crear_detalle_inventario(request): #Funcion que renderiza la pantalla de creacion de inventario
    inventario_activo = models.Inventario.objects.filter(sePuedeEditar=True).first() #obtener el inventario activo en proceso
    if inventario_activo is None:
        return redirect('ver_inventario')
    else:
        if request.method == 'POST':
            indices_keys = [key for key in request.POST.keys() if key.startswith('cantidad-')]
            for i in range(len(indices_keys)):
                detalle = models.DetalleInventario()
                detalle.idInventario = inventario_activo
                detalle.idProducto_id = request.POST['product']
                detalle.cantidadProducto = request.POST['cantidad-' + str(i+1)]
                detalle.fechaIngreso = request.POST['ingreso-' + str(i+1)][0:10].format('YYYY-MM-DD')
                detalle.horaIngreso = request.POST['ingreso-'+ str(i+1)][11:16].format('HH:MM:SS')
                detalle.fechaCaducidad = request.POST['caducidad-'+ str(i+1)].format('YYYY-MM-DD')
                detalle.save()
                urlCrearInventario = reverse('crear_inventario')
            return redirect(f'{urlCrearInventario}?exito=1')
        elif request.method == 'GET':
            fecha_inventario = inventario_activo.fechaInventario
            hora_inventario = inventario_activo.horaInventario
            return render(request, 'crear_detalle_inventario.html', {'fecha_inventario': fecha_inventario, 'hora_inventario': hora_inventario})


#Funcion para ver la informacion de un detalle de inventario, recibe el id de inventario y el id del producto
def ver_detalle_inventario(request, inventarioId=None, productoId=None):
    if productoId is not None and inventarioId is not None:
        inventario = models.Inventario.objects.get(idInventario=inventarioId)
        producto = models_productos.Producto.objects.get(idProducto=productoId)
        if inventario and producto:
            fecha_inventario = inventario.fechaInventario
            hora_inventario = inventario.horaInventario
            listadoDetalles = models.DetalleInventario.objects.all().filter(idInventario=inventario).filter(idProducto=producto)
            if listadoDetalles:
                detalles = []
                for detalle in listadoDetalles:
                    detalles.append(detalle)
                return render(request, 'ver_detalle_inventario.html', {'producto': producto, 'detalles': detalles, 'fecha_inventario': fecha_inventario, 'hora_inventario': hora_inventario, 'inventario':inventario})
    else:
        return render(request, 'ver_detalle_inventario.html')   

#Funcion para editar un detalle de inventario, recibe el id de inventario y el id del producto
#internamente tiene 3 funcionamientos, si el detalle fue recuperado del inventario anterior, si el detalle fue creado en este inventario y si se está creando actualmente el detalle
#resumido en: Anterior, Actual y Nuevo
def editar_detalle_inventario(request, inventarioId=None, productoId=None):
    if request.method == 'POST':
        print(request.POST)
        anteriores = [key for key in request.POST.keys() if key.startswith('anterior-cantidad')]
        actuales = [key for key in request.POST.keys() if key.startswith('actual-cantidad')]
        nuevos = [key for key in request.POST.keys() if key.startswith('nuevo-cantidad-')]
        
        ids = []##para guardar los id que no se borraran
        print(nuevos)
        #Este bloque es para actualizar los detalles o crear los nuevos:
        if anteriores is not None:
            for key in anteriores:
                indice = key.split('-')[2]
                detalle = models.DetalleInventario.objects.get(pk = request.POST['anterior-detalleId-' + str(indice)])
                detalle.cantidadProducto = request.POST['anterior-cantidad-' + str(indice)]
                detalle.save()
        if actuales is not None:
            for key in actuales:
                indice = key.split('-')[2]
                detalle = models.DetalleInventario.objects.get(pk = request.POST['actual-detalleId-' + str(indice)])
                detalle.cantidadProducto = request.POST['actual-cantidad-' + str(indice)]
                detalle.fechaIngreso = request.POST['actual-ingreso-' + str(indice)][0:10].format('YYYY-MM-DD')
                detalle.horaIngreso = request.POST['actual-ingreso-'+ str(indice)][11:16].format('HH:MM:SS')
                detalle.fechaCaducidad = request.POST['actual-caducidad-'+ str(indice)].format('YYYY-MM-DD')
                detalle.save()
        if nuevos:
            for key in nuevos:
                print(key)
                indice = key.split('-')[2]
                detalle = models.DetalleInventario()
                detalle.idInventario_id = inventarioId
                detalle.idProducto_id = productoId
                detalle.cantidadProducto = request.POST['nuevo-cantidad-' + str(indice)]
                detalle.fechaIngreso = request.POST['nuevo-ingreso-' +str(indice)][0:10].format('YYYY-MM-DD')
                detalle.horaIngreso = request.POST['nuevo-ingreso-'+str(indice)][11:16].format('HH:MM:SS')
                detalle.fechaCaducidad = request.POST['nuevo-caducidad-'+str(indice)].format('YYYY-MM-DD')
                detalle.save()
                ids.append(str(detalle.idDetalleInventario))
                
        #Este bloque es para gestionar la eliminacion de detalles "Actuales"
        detallesProductoInventario = models.DetalleInventario.objects.all().filter(idInventario_id=inventarioId).filter(idProducto_id=productoId)
        if anteriores:
            for key in anteriores:
                indice = key.split('-')[2]
                ids.append(request.POST['anterior-detalleId-' + str(indice)])
        if actuales:
            for key in actuales:
                indice = key.split('-')[2]
                ids.append(request.POST['actual-detalleId-' + str(indice)])
        print(ids)
        for detalle in detallesProductoInventario:
            if str(detalle.idDetalleInventario) not in ids:
                detalle.delete()
        url = reverse('crear_inventario')
        return redirect(f'{url}?exito=2')
    elif inventarioId is not None and productoId is not None:
        inventario = models.Inventario.objects.get(idInventario=inventarioId)
        if not inventario or inventario.sePuedeEditar == False: #No existe el inventario o no se puede editar
            return redirect('ver_inventario')
        else:
            producto = models_productos.Producto.objects.get(idProducto=productoId)
            if producto:
                detallesAnteriores = []
                detallesNuevos = []
                detallesProducto = models.DetalleInventario.objects.all().filter(idInventario=inventario).filter(idProducto=producto)
                if detallesProducto:
                    for detalle in detallesProducto:
                        #cantidadDetallesProducto es la cantidad de detalles del mismo producto con la misma fecha de ingreso, se usa este parametro para comparar si es anterior
                        cantidadDetallesProducto = len(models.DetalleInventario.objects.all().filter(idProducto=producto).filter(fechaIngreso=detalle.fechaIngreso).filter(fechaCaducidad=detalle.fechaCaducidad))
                        if cantidadDetallesProducto > 1:
                            detallesAnteriores.append(detalle)
                        elif cantidadDetallesProducto == 1:
                            detallesNuevos.append(detalle)
                return render(request, 'editar_detalle_inventario.html', {'producto': producto, 'detallesAnteriores': detallesAnteriores, 'detallesNuevos': detallesNuevos, 'inventario':inventario})
        
        
    
#listar inventarios, muestra los inventarios creados, ordenados por fecha de creacion
@groups_required('Jefe')
@login_required
def listar_inventario(request):
    
    inventarios = models.Inventario.objects.all().order_by('idInventario')
    paginator = Paginator(inventarios, 10)  # Cambia 10 por la cantidad que desees por página
    # Obtener el número de página desde la solicitud GET
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'listar_inventario.html', {'inventarios': page})
     


    
# Create your views here.

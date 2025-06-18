from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Gestion_Proveedores.models import Proveedor, HorarioProveedor, ProductoProveedor
from django.core.paginator import Paginator
from django.contrib import messages
from django.urls import reverse#esta importacion es para manejar la url y pasar el paremetro de validacion a js

# Create your views here.
@login_required
def registrar_proveedor(request):
    if request.method == 'POST':
        try:#incluimos el try para poder mostrar de una mejor manera los errores
            #Seccion para tabla Proveedor
            nombre_proveedor = request.POST.get('nombre_proveedor')
            apellido_proveedor = request.POST.get('apellido_proveedor')
            dui_proveedor =request.POST.get('dui_proveedor')
            correo_proveedor = request.POST.get('correo_proveedor')
            numero_proveedor = request.POST.get('numero_proveedor')
            nombre_empresa = request.POST.get('nombre_empresa')
            direccion_empresa = request.POST.get('direccion_empresa')
            logo = request.FILES.get('logo')
            iva_proveedor = 'iva_proveedor' in request.POST
            
            #Seccion de tabla horarios
            hora_apertura = request.POST.get('hora_apertura')
            hora_cierre = request.POST.get('hora_cierre')
            dias = request.POST.getlist('dias')
            dias_texto = ",".join(dias)
                   
            proveedor = Proveedor.objects.create(
                nombreEncargado = nombre_proveedor,
                apellidoEncargado = apellido_proveedor,
                nombreEmpresa = nombre_empresa,
                tieneIva = iva_proveedor,
                telProveedor = numero_proveedor,
                duiEncargado = dui_proveedor,
                emailProveedor = correo_proveedor,
                ubicacionProveedor = direccion_empresa,
                logo = logo           
            )

            HorarioProveedor.objects.create(
                idProveedor = proveedor,
                horaApertura = hora_apertura,
                horaCierre = hora_cierre,
                diaSemana = dias_texto
            )
            
            # Crear productos del proveedor
            nombres_productos = request.POST.getlist('producto_nombre[]')
            precios_productos = request.POST.getlist('producto_precio[]')

            for nombre, precio in zip(nombres_productos, precios_productos):
                ProductoProveedor.objects.create(
                    idProveedor=proveedor,
                    nombreProductoProveedor=nombre,
                    precioProductoProveedor=precio
                )


            #aca ponemos la url para que el js pueda leer el ?exito=1
            url= reverse('listar_proveedores')#guardamos el enlace principa
            return redirect(f'{url}?exito=1')#aparte del enlace principal añadimos el ?exito=1 para que js lo lea
        
        #Esta es la excepcion que cierra el try
        except Exception as e:
            #Si hay un error se mostrara este mensaje
            messages.error(request, f"Error al registrar proveedor: {e}")

            #Retornamos la misma pagina, pero el 'data': request.POST
            #sirve para poder hacer un reseteo de la data al ser post
            return render(request, 'registrar_proveedor.html', {
                'data': request.POST
            })

    return render(request, 'registrar_proveedor.html')


@login_required
def listar_proveedor(request):

    proveedores = Proveedor.objects.filter(estaHabilitadoProveedor=True).order_by('idProveedor')#objeto de proveedor ordenado por id
    paginator = Paginator(proveedores, 10) #usamos la plantilla de django para paginar los proveedores con un maximo de 10 elementos, le pasamos el elemento o listado de proveedores

    page_number = request.GET.get('page') #guardamos el # de pagina actual en la url
    page = paginator.get_page(page_number) #asignamos el numero de pagina

    return render(request, 'listar_proveedores.html', {'proveedores_paginados': page})#aca en vez de mandar un objeto de proveedores mandamos el de la paginacion que contiene tambien el listado de proveedores

#Este metodo funciona para que se deshabilite el proveedor y ya no aparezca en el cuadro de listado de proveedores, se define su respectiva url y en el html se pasa el argumento de la vista en el boton elimiar, incluyendo un mensaje de confirmación con "oneclick"
@login_required
def deshabilitar_proveedor(request, id):#se pasa de argumento el id para que exactamente en la bd busque el id de la fila de la tabla
    proveedor = get_object_or_404(Proveedor, pk=id) #mandamos el get object 404 para que si no hay id muestre que no existe la pagina
    proveedor.estaHabilitadoProveedor = False #deshabilitamos el campo de habilitacion del proveedor
    proveedor.save()
    return redirect('listar_proveedores') #se redirige a la misma vista de listar proveedores

@login_required
def detalle_proveedor(request, id_proveedor):
    proveedor = get_object_or_404(Proveedor, pk=id_proveedor) #Obtenemos el id del proveedor
    horario = HorarioProveedor.objects.filter(idProveedor=proveedor).first() #filtramos los horarios por el id del proveedor
    productos = ProductoProveedor.objects.filter(idProveedor=proveedor) #filtramos de igual manera los productos asociados por el id del proveedor

    dias_semana = {
        '1': 'Lunes',
        '2': 'Martes',
        '3': 'Miércoles',
        '4': 'Jueves',
        '5': 'Viernes',
        '6': 'Sábado',
        '7': 'Domingo'
    }

    dias_mostrados = []
    if horario and horario.diaSemana:
        numeros = horario.diaSemana.split(',')
        dias_mostrados = [dias_semana.get(num.strip(), 'Desconocido') for num in numeros]


    #Creamos un bloque de contexto para enviarle al html eso y pueda llamar cada una de las tablas
    context = {
        'proveedor': proveedor,
        'horario': horario,
        'productos': productos,
        'dias_mostrados': dias_mostrados,
    }

    return render(request, 'detalle_proveedor.html', context)


@login_required
def editar_proveedor(request, id):
    proveedor = get_object_or_404(Proveedor, pk=id)
    horario = HorarioProveedor.objects.filter(idProveedor=proveedor)
    productos = ProductoProveedor.objects.filter(idProveedor=proveedor)
    dias_guardados = []
    for h in horario:
        dias_guardados.extend(int(d) for d in h.diaSemana.split(','))
    

    if request.method == 'POST':
        proveedor.nombreEncargado = request.POST.get('nombre_proveedor')
        proveedor.apellidoEncargado = request.POST.get('apellido_proveedor')
        proveedor.nombreEmpresa = request.POST.get('nombre_empresa')
        proveedor.duiEncargado = request.POST.get('dui_proveedor')
        proveedor.telProveedor = request.POST.get('numero_proveedor')
        proveedor.emailProveedor = request.POST.get('correo_proveedor')
        proveedor.ubicacionProveedor = request.POST.get('direccion_empresa')
        proveedor.tieneIva = bool(request.POST.get('iva_proveedor'))
        if request.FILES.get('logo'):
            proveedor.logo = request.FILES['logo']
        
        proveedor.save()

        #Para horarios
        dias = request.POST.getlist('dias')
        dias_texto = ",".join(dias)        

        hora_apertura = request.POST.get('hora_apertura')
        hora_cierre = request.POST.get('hora_cierre')

        # Eliminar horarios antiguos
        horario.delete()

        HorarioProveedor.objects.create(
            idProveedor=proveedor,
            diaSemana=dias_texto,
            horaApertura=hora_apertura,
            horaCierre=hora_cierre
            )
             
        #Eliminar productos anteriores
        productos.delete()

        #Creamos el nuevo productos o lista
        nombres_productos = request.POST.getlist('producto_nombre[]')
        precios_productos = request.POST.getlist('producto_precio[]')

        for nombre, precio in zip(nombres_productos, precios_productos):
                ProductoProveedor.objects.create(
                    idProveedor=proveedor,
                    nombreProductoProveedor=nombre,
                    precioProductoProveedor=precio
                )
        return redirect('listar_proveedores')
    
    contexto ={
        'proveedor': proveedor,
        'horario': horario,
        'dias_guardados': dias_guardados,
        'productos': productos
    }

    return render(request, 'editar_proveedor.html', contexto)

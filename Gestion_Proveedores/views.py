from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Gestion_Proveedores.models import Proveedor, HorarioProveedor
from django.core.paginator import Paginator


# Create your views here.
@login_required
def registrar_proveedor(request):
    if request.method == 'POST':
        #Seccion para tabla Proveedor
        nombre_proveedor = request.POST.get('nombre_proveedor')
        apellido_proveedor = request.POST.get('apellido_proveedor')
        dui_proveedor =request.POST.get('dui_proveedor')
        correo_proveedor = request.POST.get('correo_proveedor')
        numero_proveedor = request.POST.get('numero_proveedor')
        nombre_empresa = request.POST.get('nombre_empresa')
        direccion_empresa = request.POST.get('direccion_empresa')
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
        )

        HorarioProveedor.objects.create(
            idProveedor = proveedor,
            horaApertura = hora_apertura,
            horaCierre = hora_cierre,
            diaSemana = dias_texto
        )

        return redirect('listar_proveedores')


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

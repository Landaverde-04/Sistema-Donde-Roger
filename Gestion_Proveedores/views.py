from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from Gestion_Proveedores.models import Proveedor, HorarioProveedor


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

    proveedores = Proveedor.objects.all()

    return render(request, 'listar_proveedores.html', {'proveedores': proveedores})


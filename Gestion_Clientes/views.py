from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required
from Gestion_Clientes.models import Cliente
from django.urls import reverse
from django.core.paginator import Paginator #para paginar

# Create your views here.

@groups_required('Jefe', 'Gerente')
@login_required
def registrar_cliente(request):

    if request.method == 'POST':    
        nombre_cliente = request.POST.get('nombre')
        apellidos_cliente = request.POST.get('apellidos')
        dui_cliente = request.POST.get('dui')
        telefono_cliente = request.POST.get('telefono')
        correo_cliente = request.POST.get('correo')
        fecha_nacimiento_cliente = request.POST.get('fecha_nacimiento')
        
        Cliente.objects.create(
            nombreCliente = nombre_cliente,
            apellidoCliente = apellidos_cliente,
            duiCliente = dui_cliente,
            telefonoCliente = telefono_cliente,
            emailCliente = correo_cliente,
            nacimientoCliente = fecha_nacimiento_cliente            
        )
        url = reverse('listar_clientes')
        return redirect(f'{url}?exito=1')
    return render(request, 'registrar_cliente.html')

def listar_clientes(request):
    clientes = Cliente.objects.filter(estaHabilitadoCliente=True)
    clientes = clientes.order_by('idCliente')
    paginator = Paginator(clientes, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'listar_clientes.html',
                  {'clientes_paginados': page})
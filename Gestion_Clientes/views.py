from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required
from Gestion_Clientes.models import Cliente, DireccionCliente
from django.urls import reverse
from django.core.paginator import Paginator #para paginar
from django.db.models import Q
# Create your views here.


@login_required
def registrar_cliente(request):

    if request.method == 'POST':    
        nombre_cliente = request.POST.get('nombre')
        apellidos_cliente = request.POST.get('apellidos')
        dui_cliente = request.POST.get('dui')
        telefono_cliente = request.POST.get('telefono')
        correo_cliente = request.POST.get('correo')
        fecha_nacimiento_cliente = request.POST.get('fecha_nacimiento')

        direccion = request.POST.getlist("direccion_cliente")
        
        cliente = Cliente.objects.create(
            nombreCliente = nombre_cliente,
            apellidoCliente = apellidos_cliente,
            duiCliente = dui_cliente,
            telefonoCliente = telefono_cliente,
            emailCliente = correo_cliente,
            nacimientoCliente = fecha_nacimiento_cliente            
        )

        for direcciones in direccion:
            direcciones = direcciones.strip()  # Eliminar espacios en blanco al inicio y al final
            if direcciones:  # Verificar que la dirección no esté vacía
                DireccionCliente.objects.create(
                    idCliente = cliente,
                    direccion = direcciones
                )

        url = reverse('listar_clientes')
        return redirect(f'{url}?exito=1')
    return render(request, 'registrar_cliente.html', {
        'data' : request.POST
    })

@login_required
def listar_clientes(request):
    clientes = Cliente.objects.filter(estaHabilitadoCliente=True)
    query = request.GET.get('q', '')

    if query:
        clientes = clientes.filter(
            Q(nombreCliente__icontains=query) | 
            Q(apellidoCliente__icontains=query) | 
            Q(emailCliente__icontains=query))
        paginator = Paginator(clientes, 10)

    clientes = clientes.order_by('idCliente')
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'listar_clientes.html',
                  {'clientes_paginados': page,
                  'query': query
                  })

def deshabilitar_cliente(request, id):
    cliente = Cliente.objects.get(idCliente=id)
    cliente.estaHabilitadoCliente = False
    cliente.save()
    
    return redirect('listar_clientes')

@groups_required('Jefe', 'Gerente')
@login_required
def listar_clientes_deshabilitados(request):
    clientes = Cliente.objects.filter(estaHabilitadoCliente=False)
    query = request.GET.get('q', '')

    if query:
        clientes = clientes.filter(
            Q(nombreCliente__icontains=query) | 
            Q(apellidoCliente__icontains=query) | 
            Q(emailCliente__icontains=query))
        paginator = Paginator(clientes, 10)

    clientes = clientes.order_by('idCliente')
    paginator = Paginator(clientes, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'listar_clientes_deshabilitados.html',
                  {'clientes_paginados': page,
                  'query': query
                  })

@groups_required('Jefe', 'Gerente')
@login_required
def habilitar_cliente(request, id):
    cliente = Cliente.objects.get(idCliente=id)
    cliente.estaHabilitadoCliente = True
    cliente.save()
    
    return redirect('listar_clientes_deshabilitados')
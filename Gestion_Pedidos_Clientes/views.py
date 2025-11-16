from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from Gestion_Menu.models import CategoriaProductoMenu, ProductoMenu
from Gestion_Clientes.models import *
from django.db.models import Prefetch, Q
from Gestion_Pedidos_Clientes.models import *
import datetime
import json
from django.http import JsonResponse

# Create your views here.

def api_clientes(request):
    if request.GET:
        nombres = request.GET.get("names") if request.GET.get("names") != "undefined" else None
        page = int(request.GET.get("page", 1))
        per_page = int(request.GET.get("per_page", 5))
        if nombres:
            queryset = Cliente.objects.filter(
                Q(nombreCliente__icontains=nombres) |
                Q(apellidoCliente__icontains=nombres)|
                Q(telefonoCliente__icontains=nombres)
            ).values(
                "idCliente", "nombreCliente", "apellidoCliente",
                "duiCliente", "telefonoCliente", "emailCliente",
                "nacimientoCliente"
            )
        elif request.GET.get("idCliente"):
            queryset = Cliente.objects.filter(idCliente=request.GET.get("idCliente")).values(
                "idCliente", "nombreCliente", "apellidoCliente",
                "duiCliente", "telefonoCliente", "emailCliente",
                "nacimientoCliente"
            )
        else:
            queryset = Cliente.objects.all().values(
                "idCliente", "nombreCliente", "apellidoCliente",
                "duiCliente", "telefonoCliente", "emailCliente",
                "nacimientoCliente"
            )

        paginator = Paginator(queryset, per_page)
        page_obj = paginator.get_page(page)
        return JsonResponse({
            "results": list(page_obj),
            "page": page_obj.number,
            "total_pages": paginator.num_pages,
            "total_items": paginator.count,
        })
    elif request.POST:
        print(request.POST)
        cliente = Cliente()
        cliente.nombreCliente = request.POST.get('nombreCliente')
        cliente.apellidoCliente = request.POST.get('apellidoCliente')
        cliente.duiCliente = request.POST.get('duiCliente')
        cliente.telefonoCliente = request.POST.get('telefonoCliente')
        cliente.emailCliente = request.POST.get('emailCliente')
        cliente.nacimientoCliente = request.POST.get('nacimientoCliente') if len(request.POST.get('nacimientoCliente'))>0 else None
        cliente.save()
        return JsonResponse({
            "idCliente": cliente.idCliente,
            "nombreCliente": cliente.nombreCliente,
            "apellidoCliente": cliente.apellidoCliente,
            "duiCliente": cliente.duiCliente,
            "telefonoCliente": cliente.telefonoCliente,
            "emailCliente": cliente.emailCliente,
            "nacimientoCliente": cliente.nacimientoCliente,
        })
    return JsonResponse({"error": "Método no permitido"}, status=400)


def api_direcciones(request):
    idCliente = request.GET.get("idCliente")
    direcciones = DireccionCliente.objects.filter(idCliente=idCliente).values("direccion")
    return JsonResponse({
        "results": list(direcciones),
    })

# Create your views here.

def crear_pedido(request):
    if request.method == 'GET':
        categorias_con_productos = (CategoriaProductoMenu.objects.filter(
        productomenu__estaHabilitadoProductoMenu=True).distinct().prefetch_related(
        Prefetch('productomenu_set',queryset=ProductoMenu.objects.filter(estaHabilitadoProductoMenu=True))))
        numCorrelativo = PedidoCliente.objects.filter(fechaPedidoCliente=datetime.date.today()).count() + 1
        return render(request, 'crear_pedido.html', {'categorias_con_productos':categorias_con_productos, 'numCorrelativo':numCorrelativo})
    elif request.method == 'POST':
        print(request.POST)
        pedido = PedidoCliente()
        pedido.fechaPedidoCliente = datetime.date.today()
        pedido.horaPedidoCliente = datetime.datetime.now()
        pedido.numCorrelativo = request.POST.get('num-correlativo')
        pedido.totalPedido = 0
        tipoPedido = request.POST.get('tipoPedido')
        pedido.tipoPedido = TipoPedidoCliente.objects.get(idTipoPedido=tipoPedido)
        pedido.estadoPedido = EstadoPedidoCliente.objects.get(idEstado=1)
        if request.POST.get('idCliente'):
            pedido.idCliente = Cliente.objects.get(idCliente=request.POST.get('idCliente'))
        if tipoPedido == '1':
            pedido.mesasPedido = request.POST.get('mesa')
        elif tipoPedido == '2':
            pedido.horaRecoger = request.POST.get('hora-recoger')
        elif tipoPedido == '3':
            direccion = request.POST.get('direccion-nueva') if len(request.POST.get('direccion-nueva')) > 0 else request.POST.get('direccion')
            if request.POST.get('esNuevaDireccion') == 'on':
                direccion = request.POST.get('direccion-nueva')
                nuevaDireccion = DireccionCliente()
                nuevaDireccion.idCliente = pedido.idCliente
                nuevaDireccion.direccion = direccion
                nuevaDireccion.save()
                pedido.direccionPedido = direccion
            elif request.POST.get('esNuevaDireccion') == 'off':
                direccion = request.POST.get('direccion')
            pedido.direccionPedido = direccion
        pedido.save()
        detalles_json = request.POST.get('detalles-pedido')
        detalles = json.loads(detalles_json)
        for detalle in detalles:
            nuevoDetalle = DetallePedido()
            nuevoDetalle.idPedidoCliente = pedido
            nuevoDetalle.idProducto = ProductoMenu.objects.get(idProductoMenu=detalle["idProductoMenu"])
            nuevoDetalle.cantidadPedido = detalle["cantidadPedido"]
            nuevoDetalle.subtotalPedido = detalle["subtotalPedido"]
            pedido.totalPedido += detalle["subtotalPedido"]
            nuevoDetalle.save()
            pedido.save()
        return redirect('crear_pedido')

def ver_pedido(request, idPedido):
    if not idPedido or not idPedido.isdigit() or int(idPedido) < 1:
        return redirect(reverse('listar_pedidos'))
    pedido = PedidoCliente.objects.get(idPedidoCliente=idPedido)
    detalles = DetallePedido.objects.filter(idPedidoCliente=idPedido)
    return render(request, 'ver_pedido.html', {'pedido':pedido, 'detalles':detalles})

def actualizar_estado_pedido(request, idPedido):
    if not idPedido or not idPedido.isdigit() or int(idPedido) < 1:
        return redirect(reverse('listar_pedidos'))
    pedido = PedidoCliente.objects.get(idPedidoCliente=idPedido)
    estadoActual = pedido.estadoPedido.idEstado
    if pedido.tipoPedido.idTipoPedido == 1:
        if estadoActual == 1:
            estadoSiguiente = 2
        else:
            estadoSiguiente = 5
    elif pedido.tipoPedido.idTipoPedido == 2:
        if estadoActual == 1:
            estadoSiguiente = 3
        else:
            estadoSiguiente = 5
    elif pedido.tipoPedido.idTipoPedido == 3:
        if estadoActual == 1:
            estadoSiguiente = 4
        else:
            estadoSiguiente = 6
    pedido.estadoPedido = EstadoPedidoCliente.objects.get(idEstado=estadoSiguiente)
    pedido.save()
    return redirect(reverse('ver_pedido', kwargs={'idPedido':idPedido}))

def listar_pedidos(request):
    pedidos = PedidoCliente.objects.all().order_by('fechaPedidoCliente')
    return render(request, 'listar_pedidos.html', {'pedidos':pedidos})

def listar_pedidos_hoy(request):
    pedidos = PedidoCliente.objects.filter(fechaPedidoCliente=datetime.date.today()).order_by('fechaPedidoCliente')
    return render(request, 'listar_pedidos_hoy.html', {'pedidos':pedidos})


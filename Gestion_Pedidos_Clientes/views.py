from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from Gestion_Menu.models import CategoriaProductoMenu, ProductoMenu
from Gestion_Clientes.models import Cliente
from django.db.models import Prefetch, Q
from Gestion_Pedidos_Clientes.models import *
import datetime
import json
from django.http import JsonResponse

# Create your views here.

def api_clientes(request):
    nombres = request.GET.get("names") if request.GET.get("names") != "undefined" else None
    page = int(request.GET.get("page", 1))
    per_page = int(request.GET.get("per_page", 5))
    if nombres:
        queryset = Cliente.objects.filter(
            Q(nombreCliente__icontains=nombres) |
            Q(apellidoCliente__icontains=nombres)
        ).values(
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
        pedido.tipoPedido = TipoPedidoCliente.objects.get(idTipoPedido=request.POST.get('tipoPedido'))
        pedido.estadoPedido = EstadoPedidoCliente.objects.get(idEstado=1)
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
        return redirect('crear_pedido')

def listar_pedidos(request):
    pedidos = PedidoCliente.objects.all().order_by('fechaPedidoCliente')
    return render(request, 'listar_pedidos.html', {'pedidos':pedidos})


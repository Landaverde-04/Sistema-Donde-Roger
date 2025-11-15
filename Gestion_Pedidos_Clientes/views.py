from django.shortcuts import render, redirect
from Gestion_Menu.models import CategoriaProductoMenu, ProductoMenu
from Gestion_Clientes.models import Cliente
from django.db.models import Prefetch
from Gestion_Pedidos_Clientes.models import *
import datetime
import json
from django.http import JsonResponse

# Create your views here.

def api_clientes(request):
    clientes = Cliente.objects.all().values(
        'idCliente', 
        'duiCliente', 
        'nombreCliente',
        'telefonoCliente',
        'direccionCliente'
    )
    return JsonResponse(list(clientes), safe=False)

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


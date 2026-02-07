from django.shortcuts import render, redirect
from django.urls import reverse
from django.core.paginator import Paginator
from Gestion_Menu.models import CategoriaProductoMenu, ProductoMenu
from Gestion_Clientes.models import *
from django.db.models import Prefetch, Q
from Gestion_Pedidos_Clientes.models import *
import datetime
import json
from django.http import JsonResponse, HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.conf import settings
import os

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
                Q(telefonoCliente__icontains=nombres),
                estaHabilitadoCliente=True
            ).values(
                "idCliente", "nombreCliente", "apellidoCliente",
                "duiCliente", "telefonoCliente", "emailCliente",
                "nacimientoCliente"
            )
        elif request.GET.get("idCliente"):
            queryset = Cliente.objects.filter(idCliente=request.GET.get("idCliente"), estaHabilitadoCliente=True).values(
                "idCliente", "nombreCliente", "apellidoCliente",
                "duiCliente", "telefonoCliente", "emailCliente",
                "nacimientoCliente"
            )
        else:
            queryset = Cliente.objects.filter(estaHabilitadoCliente=True).values(
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
        return render(request, 'crear_pedido.html', {
            'categorias_con_productos': categorias_con_productos, 
            'numCorrelativo': numCorrelativo,
            'today': datetime.date.today()
        })
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
        
        # Asociar cliente si existe
        if request.POST.get('idCliente'):
            pedido.idCliente = Cliente.objects.get(idCliente=request.POST.get('idCliente'))
        
        # Configurar campos específicos según tipo de pedido
        if tipoPedido == '1':
            # En restaurante
            pedido.mesasPedido = request.POST.get('mesa')
        elif tipoPedido == '2':
            # Cliente recogerá
            hora_recoger = request.POST.get('hora-recoger')
            if hora_recoger:
                # El campo datetime-local viene en formato: YYYY-MM-DDTHH:MM
                pedido.horaRecoger = datetime.datetime.strptime(hora_recoger, '%Y-%m-%dT%H:%M')
        elif tipoPedido == '3':
            # A domicilio
            direccion = request.POST.get('direccion-nueva') if request.POST.get('direccion-nueva') else request.POST.get('direccion')
            
            # Solo guardar nueva dirección si hay cliente asociado
            if pedido.idCliente and request.POST.get('esNuevaDireccion') == 'on' and request.POST.get('direccion-nueva'):
                nuevaDireccion = DireccionCliente()
                nuevaDireccion.idCliente = pedido.idCliente
                nuevaDireccion.direccion = request.POST.get('direccion-nueva')
                nuevaDireccion.save()
            
            pedido.direccionPedido = direccion
        
        # Agregar comentarios si existen
        comentarios = request.POST.get('comentarios')
        if comentarios:
            pedido.comentario = comentarios
        
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
    pedidos = PedidoCliente.objects.all().order_by('-fechaPedidoCliente', '-horaPedidoCliente')
    query = request.GET.get('q', '').strip()
    
    if query:
        # Dividir el query en palabras para buscar mejor
        palabras = query.split()
        q_filter = Q(numCorrelativo__icontains=query)
        
        # Si hay una sola palabra, buscar en nombre o apellido
        if len(palabras) == 1:
            q_filter |= Q(idCliente__nombreCliente__icontains=palabras[0])
            q_filter |= Q(idCliente__apellidoCliente__icontains=palabras[0])
        # Si hay dos o más palabras, buscar combinaciones
        elif len(palabras) >= 2:
            # Buscar primera palabra en nombre y resto en apellido
            for i in range(len(palabras)):
                nombre_parte = ' '.join(palabras[:i+1])
                apellido_parte = ' '.join(palabras[i+1:]) if i+1 < len(palabras) else ''
                
                q_nombre = Q(idCliente__nombreCliente__icontains=nombre_parte)
                if apellido_parte:
                    q_nombre &= Q(idCliente__apellidoCliente__icontains=apellido_parte)
                q_filter |= q_nombre
                
                # También buscar cada palabra individualmente
                q_filter |= Q(idCliente__nombreCliente__icontains=palabras[i])
                q_filter |= Q(idCliente__apellidoCliente__icontains=palabras[i])
        
        pedidos = pedidos.filter(q_filter)
    
    return render(request, 'listar_pedidos.html', {'pedidos': pedidos, 'query': query})

def listar_pedidos_hoy(request):
    pedidos = PedidoCliente.objects.filter(fechaPedidoCliente=datetime.date.today()).order_by('-horaPedidoCliente')
    query = request.GET.get('q', '').strip()
    
    if query:
        # Dividir el query en palabras para buscar mejor
        palabras = query.split()
        q_filter = Q(numCorrelativo__icontains=query)
        
        # Si hay una sola palabra, buscar en nombre o apellido
        if len(palabras) == 1:
            q_filter |= Q(idCliente__nombreCliente__icontains=palabras[0])
            q_filter |= Q(idCliente__apellidoCliente__icontains=palabras[0])
        # Si hay dos o más palabras, buscar combinaciones
        elif len(palabras) >= 2:
            # Buscar primera palabra en nombre y resto en apellido
            for i in range(len(palabras)):
                nombre_parte = ' '.join(palabras[:i+1])
                apellido_parte = ' '.join(palabras[i+1:]) if i+1 < len(palabras) else ''
                
                q_nombre = Q(idCliente__nombreCliente__icontains=nombre_parte)
                if apellido_parte:
                    q_nombre &= Q(idCliente__apellidoCliente__icontains=apellido_parte)
                q_filter |= q_nombre
                
                # También buscar cada palabra individualmente
                q_filter |= Q(idCliente__nombreCliente__icontains=palabras[i])
                q_filter |= Q(idCliente__apellidoCliente__icontains=palabras[i])
        
        pedidos = pedidos.filter(q_filter)
    
    return render(request, 'listar_pedidos_hoy.html', {'pedidos': pedidos, 'query': query})


def generar_pdf_pedido(request, idPedido):
    if not idPedido or not idPedido.isdigit() or int(idPedido) < 1:
        return redirect(reverse('listar_pedidos'))
    
    # Obtener datos del pedido
    pedido = PedidoCliente.objects.get(idPedidoCliente=idPedido)
    detalles = DetallePedido.objects.filter(idPedidoCliente=idPedido)
    
    # Renderizar template HTML
    template = get_template('pedido_cliente_pdf.html')
    logo_path = os.path.join(settings.MEDIA_ROOT, 'logo-Donde-Roger.jpg')
    context = {
        'pedido': pedido, 
        'detalles': detalles,
        'logo_path': logo_path
    }
    html = template.render(context)
    
    # Crear PDF con función de link para imágenes locales
    pdf_file = BytesIO()
    pisa_status = pisa.CreatePDF(
        html, 
        dest=pdf_file,
        link_callback=lambda uri, rel: os.path.join(settings.MEDIA_ROOT, uri.replace(settings.MEDIA_URL, ""))
    )
    
    if pisa_status.err:
        return HttpResponse('Error al generar PDF <pre>' + html + '</pre>')
    
    # Retornar respuesta con PDF
    response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="pedido_{pedido.numCorrelativo}.pdf"'
    return response

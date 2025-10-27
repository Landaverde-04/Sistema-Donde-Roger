from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from Gestion_Proveedores.models import Proveedor, ProductoProveedor
from Gestion_compra_productos.models import PedidoProveedor, DetallePedidoProveedor
from seguridad.decoradores import groups_required
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.core.files.base import ContentFile


@groups_required('Jefe', 'Gerente')
@login_required
def crear_solicitud_compra(request):
    proveedores = Proveedor.objects.filter(estaHabilitadoProveedor=True)

    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')

        if not proveedor_id or not productos:
            messages.error(request, "Debe seleccionar un proveedor y al menos un producto.")
        else:
            proveedor = get_object_or_404(Proveedor, idProveedor=proveedor_id)
            pedido = PedidoProveedor.objects.create(proveedor=proveedor)

            for i in range(len(productos)):
                producto = get_object_or_404(ProductoProveedor, id=productos[i])
                cantidad = int(cantidades[i])
                DetallePedidoProveedor.objects.create(
                    pedido=pedido,
                    producto=producto,
                    cantidadPP=cantidad
                )

            messages.success(request, "Solicitud de compra creada correctamente.")
            return redirect('preview_solicitud_compra')  # opcional

    return render(request, 'crear_solicitud_compra.html', {'proveedores': proveedores})

@login_required
def obtener_productos(request, id_proveedor):
    productos = ProductoProveedor.objects.filter(idProveedor__idProveedor=id_proveedor)
    data = {'productos': [{'id': p.id, 'nombre': p.nombreProductoProveedor} for p in productos]}
    return JsonResponse(data)

@groups_required('Jefe', 'Gerente')
@login_required
def preview_solicitud_compra(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')

        if not proveedor_id or not productos:
            messages.error(request, "Debe seleccionar un proveedor y al menos un producto.")
            return redirect('crear_solicitud_compra')

        proveedor = get_object_or_404(Proveedor, idProveedor=proveedor_id)
        detalle_preview = []
        total_preview = 0

        for i in range(len(productos)):
            producto = get_object_or_404(ProductoProveedor, id=productos[i])
            cantidad = int(cantidades[i])
            subtotal = cantidad * producto.precioProductoProveedor
            total_preview += subtotal
            detalle_preview.append({
                'producto': producto,
                'cantidad': cantidad,
                'subtotal': subtotal
            })

        context = {
            'proveedor': proveedor,
            'detalle_preview': detalle_preview,
            'total_preview': total_preview,
            'form_data': request.POST
        }
        return render(request, 'preview_solicitud.html', context)

    return redirect('crear_solicitud_compra')


@groups_required('Jefe', 'Gerente')
@login_required
def guardar_y_generar_pdf(request):
    if request.method == 'POST':
        proveedor_id = request.POST.get('proveedor')
        productos = request.POST.getlist('producto[]')
        cantidades = request.POST.getlist('cantidad[]')

        if not proveedor_id or not productos:
            messages.error(request, "No hay datos para guardar.")
            return redirect('crear_solicitud_compra')

        proveedor = get_object_or_404(Proveedor, idProveedor=proveedor_id)
        pedido = PedidoProveedor.objects.create(proveedor=proveedor)

        for i in range(len(productos)):
            producto = get_object_or_404(ProductoProveedor, id=productos[i])
            cantidad = int(cantidades[i])
            DetallePedidoProveedor.objects.create(
                pedido=pedido,
                producto=producto,
                cantidadPP=cantidad
            )
        
        # Generar PDF en memoria
        template = get_template('pedido_pdf.html')
        context = {'pedido': pedido, 'detalles': pedido.detalles.all(),}
        html = template.render(context)
        pdf_file = BytesIO()
        pisa_status = pisa.CreatePDF(html, dest=pdf_file)
        
        if pisa_status.err:
            return HttpResponse('Error al generar PDF <pre>' + html + '</pre>')

        # Guardar PDF en un campo del modelo o en media/
        pedido.pdf_pedido.save(
            f'pedido_{pedido.idPedidoProveedor}.pdf',
            ContentFile(pdf_file.getvalue())
        )
        pedido.save()

        messages.success(request, "PDF generado y guardado correctamente.")
        return redirect('crear_solicitud_compra')

from django.shortcuts import render
from .models import Producto
from Gestion_Inventario.models import DetalleInventario
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from seguridad.decoradores import groups_required
from django.contrib import messages


# Create your views here.
# viem de registrar un producto
@groups_required('Jefe')
@login_required
def registrar_producto(request):
    if request.method == 'POST':
        #proceso para registrar un producto
        # Asegúrate de que los campos del formulario coincidan con los del modelo Producto
        # producto = Producto() Definimos un objeto Producto para guardar los datos 
        # producto.nombreProducto = request.POST.get('nombre')
        # producto.unidadMedida = request.POST.get('unidad_medida')
        # producto.marcaProducto = request.POST.get('marca')
        # producto.descripcionProducto = request.POST.get('descripcion')
        # producto.save()
        nombre = request.POST.get('nombre')
        unidad_medida = request.POST.get('unidadMedida')
        marca = request.POST.get('marcaProducto')
        descripcion = request.POST.get('descripcionProducto')
        producto = Producto()
        producto.nombreProducto = nombre
        producto.unidadMedida = unidad_medida
        producto.marcaProducto = marca
        producto.descripcionProducto = descripcion
        producto.estaHabilitadoProveedor = True  # Asignamos el estado de habilitación por defecto
        # Guarda el producto en la base de datos
        producto.save()
        # el request es el objeto de la solicitud HTTP que contiene los datos del formulario
        messages.success(request, "¡Producto registrado exitosamente!", extra_tags='producto')
        return redirect('listar_productos')

    return render(request, 'registrar_producto.html')

# Vista para registrar un producto
@groups_required('Jefe')
@login_required
def listar_productos(request):
    # Obtenemos el nombre del producto desde la solicitud GET
    # Utilizamos strip() para eliminar espacios en blanco al inicio y al final
    nombre = request.GET.get('nombre', '').strip()
    productos = Producto.objects.filter(estaHabilitadoProducto=True)
    if nombre:
        # Filtramos los productos por nombre si se proporciona
        # el nombreProducto_icontains permite buscar de manera insensible a mayúsculas y minúsculas es de Django
        productos = productos.filter(nombreProducto__icontains=nombre)
    productos = productos.order_by('idProducto')
    paginator = Paginator(productos, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'listar_productos.html', {'productos': page, 'nombre': nombre})

## Vista para actualizar un producto
@groups_required('Jefe')
@login_required
def actualizar_producto(request, producto_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        unidad_medida = request.POST.get('unidadMedida')
        marca = request.POST.get('marcaProducto')
        descripcion = request.POST.get('descripcionProducto')
        #aqui obtenemos el producto por ID y actualizamos sus campos
        producto = Producto.objects.get(idProducto=producto_id)
        producto.nombreProducto = nombre
        producto.unidadMedida = unidad_medida
        producto.marcaProducto = marca
        producto.descripcionProducto = descripcion
        producto.estaHabilitadoProducto = True
        producto.save()
        # Mensaje de éxito
        messages.success(request, "¡Producto actualizado exitosamente!", extra_tags='producto')
        return redirect('listar_productos')
    
    producto = Producto.objects.get(idProducto=producto_id)
    return render(request, 'actualizar_producto.html', {'producto': producto})

## Vista para eliminar un producto
@groups_required('Jefe')
@login_required
def eliminar_producto(request, producto_id):
    if request.method == 'POST':
        producto = Producto.objects.get(idProducto=producto_id)
        producto.estaHabilitadoProducto = False  # Deshabilitamos el producto en lugar de eliminarlo
        producto.save()
        
        return redirect('listar_productos')
    else:
        # Si no es una solicitud GET, redirigimos a la lista de productos
        return redirect('listar_productos')
    
# Vista para ver los detalles de un producto
@groups_required('Jefe')
@login_required
def detalle_producto(request, producto_id):
    producto = Producto.objects.get(idProducto=producto_id)
    if producto is not None:
        detalle_producto = DetalleInventario.objects.filter(idProducto=producto_id)
        stock = obtener_stock_actual(detalle_producto)
        return render(request, 'detalle_producto.html', {'producto': producto, 'stock': stock})


##FUNCION PARA CREAR LA SUMATORIA DE STOCK PARA LOS DETALLES DE INVENTARIO
def obtener_stock_actual(queryset):

    #Devuelve el stock actual del producto, es decir, la cantidad del último movimiento registrado.
    ultimo = queryset.order_by('-idDetalleInventario').first()
    return ultimo.cantidadProducto if ultimo else 0
from django.shortcuts import render
from .models import Producto
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator


# Create your views here.
# viem de registrar un producto
@login_required
def registrar_producto(request):
    if request.method == 'POST':
        # Aquí podrías manejar la lógica para registrar un producto
        # Por ejemplo, guardar los datos del formulario en la base de datos
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
        # Asegúrate de que los campos del formulario coincidan con los del modelo Producto
        producto.nombreProducto = nombre
        producto.unidadMedida = unidad_medida
        producto.marcaProducto = marca
        producto.descripcionProducto = descripcion
        producto.estaHabilitadoProveedor = True  # Asignamos el estado de habilitación por defecto
        # Guarda el producto en la base de datos
        producto.save()
        return redirect('listar_productos')

    return render(request, 'registrar_producto.html')

# Vista para registrar un producto
@login_required
def listar_productos(request):
    productos = Producto.objects.filter(estaHabilitadoProducto=True).order_by('idProducto')
    paginator = Paginator(productos, 10)  # Cambia 10 por la cantidad que desees por página
    # Obtener el número de página desde la solicitud GET
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'listar_productos.html', {'productos': page})

## Vista para actualizar un producto
@login_required
def actualizar_producto(request, producto_id):
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        unidad_medida = request.POST.get('unidadMedida')
        marca = request.POST.get('marcaProducto')
        descripcion = request.POST.get('descripcionProducto')
        # Aquí podrías manejar la lógica para actualizar un producto
        # Por ejemplo, buscar el producto por ID y actualizar sus campos
        producto = Producto.objects.get(idProducto=producto_id)
        producto.nombreProducto = nombre
        producto.unidadMedida = unidad_medida
        producto.marcaProducto = marca
        producto.descripcionProducto = descripcion
        producto.estaHabilitadoProducto = True  # Asegúrate de que el producto esté habilitado
        producto.save()
        return redirect('listar_productos')
    
    # Aquí podrías obtener el producto por ID de la base de datos
    producto = Producto.objects.get(idProducto=producto_id)
    return render(request, 'actualizar_producto.html', {'producto': producto})
## Vista para eliminar un producto
@login_required
def eliminar_producto(request, producto_id):
    if request.method == 'post':
        # Aquí podrías manejar la lógica para eliminar un producto
        producto = Producto.objects.get(idProducto=producto_id)
        producto.estaHabilitadoProducto = False  # Deshabilitamos el producto en lugar de eliminarlo
        producto.save()
        
        return redirect('listar_productos')
    else:
        # Si no es una solicitud GET, redirigimos a la lista de productos
        return redirect('listar_productos')
# Vista para ver los detalles de un producto
@login_required
def detalle_producto(request, producto_id):
    producto = Producto.objects.get(idProducto=producto_id)

    return render(request, 'detalle_producto.html', {'producto': producto})

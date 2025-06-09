from django.shortcuts import render
from .models import Producto
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
# viem de registrar un producto
@login_required
def registrar_producto(request):
    if request.method == 'POST':
        # Aquí podrías manejar la lógica para registrar un producto
        # Por ejemplo, guardar los datos del formulario en la base de datos
        # Asegúrate de que los campos del formulario coincidan con los del modelo Producto
        # producto = Producto() 
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
        # Guarda el producto en la base de datos
        producto.save()
        return redirect('listar_productos')

    return render(request, 'registrar_producto.html')

# Vista para registrar un producto
@login_required
def listar_productos(request):
    if request.method == 'POST':
        # Aquí podrías manejar la lógica para registrar un producto
        # Por ejemplo, guardar los datos del formulario en la base de datos
        pass
    
    # Aquí podrías obtener los productos de la base de datos
    # productos = Producto.objects.all()
    productos = Producto.objects.all()
    return render(request, 'listar_productos.html', {'productos': productos})

## Vista para actualizar un producto
@login_required
def actualizar_producto(request, producto_id):
    if request.method == 'POST':
        # Aquí podrías manejar la lógica para actualizar un producto
        # Por ejemplo, buscar el producto por ID y actualizar sus datos
        pass
    
    # Aquí podrías obtener el producto por ID de la base de datos
    # producto = Producto.objects.get(id=producto_id)
    producto = None
    return render(request, 'actualizar_producto.html', {'producto': producto})
## Vista para eliminar un producto
@login_required
def eliminar_producto(request, producto_id):
    if request.method == 'POST':
        # Aquí podrías manejar la lógica para eliminar un producto
        # Por ejemplo, buscar el producto por ID y eliminarlo de la base de datos
        pass
    
    # Aquí podrías obtener el producto por ID de la base de datos
    # producto = Producto.objects.get(id=producto_id)
    producto = None
    return render(request, 'eliminar_producto.html', {'producto': producto})
# Vista para ver los detalles de un producto
@login_required
def detalle_producto(request, producto_id):
    # Aquí podrías obtener el producto por ID de la base de datos
    # producto = Producto.objects.get(id=producto_id)
    producto = None
    return render(request, 'detalle_producto.html', {'producto': producto})
from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required
from . import models
import ast

#API REST PARA PRODUCTOS DEL MENU
def api_producto_menu(request):
    if request.method == "GET":
        nombre = request.GET.get('nombre')
        categoria = request.GET.get('categoria')
        habilitado = ast.literal_eval(request.GET.get('habilitado'))
        productos = models.ProductoMenu.objects.filter(estaHabilitadoProductoMenu=habilitado)
        if nombre:
            productos = productos.filter(nombreProductoMenu__icontains=nombre)
        if categoria:
            productos = productos.filter(idCategoriaProductoMenu=categoria)
        productos = list(productos.values())
    return JsonResponse(productos, safe=False)

def api_categorias_producto_menu(request):
    if request.method == "GET":
        categorias = list(models.CategoriaProductoMenu.objects.all().values())
    return JsonResponse(categorias, safe=False)

#CONTROLADOR PARA REGISTRO DE PRODUCTOS PARA MENU
def registrar_producto_menu(request):
    if request.method == "POST":
        print(request.POST)
        
        # Obtener y validar datos
        nombre = request.POST.get("nombre-producto", "").strip()
        tamanio = request.POST.get("tamanio-producto", "").strip()
        descripcion = request.POST.get("descripcion-producto", "").strip()
        precio = request.POST.get("precio-producto", "").strip()
        categoriaId = request.POST.get("categoria-producto", "").strip()
        
        errores = []
        
        # Validar nombre
        if not nombre:
            errores.append("El nombre del producto es requerido.")
        elif len(nombre) < 3 or len(nombre) > 50:
            errores.append("El nombre debe tener entre 3 y 50 caracteres.")
        
        # Validar tamaño/unidad
        if not tamanio:
            errores.append("La unidad/tamaño es requerida.")
        elif len(tamanio) < 2 or len(tamanio) > 50:
            errores.append("La unidad/tamaño debe tener entre 2 y 50 caracteres.")
        
        # Validar descripción
        if descripcion and len(descripcion) > 500:
            errores.append("La descripción no puede exceder 500 caracteres.")
        
        # Validar precio
        if not precio:
            errores.append("El precio es requerido.")
        else:
            try:
                precio_decimal = float(precio)
                if precio_decimal <= 0:
                    errores.append("El precio debe ser mayor a 0.")
                elif precio_decimal > 9999.99:
                    errores.append("El precio no puede exceder 9999.99.")
            except ValueError:
                errores.append("El precio debe ser un número válido.")
        
        # Validar categoría
        if not categoriaId:
            errores.append("Debe seleccionar una categoría.")
        
        # Si hay errores, retornar al formulario
        if errores:
            categorias = models.CategoriaProductoMenu.objects.all()
            return render(request, 'registrar_producto_menu.html', {
                'categorias': categorias,
                'error': ' '.join(errores),
                'nombre': nombre,
                'tamanio': tamanio,
                'descripcion': descripcion,
                'precio': precio
            })
        
        # Intentar crear el producto
        try:
            producto = models.ProductoMenu()
            producto.nombreProductoMenu = nombre
            producto.tamanioProductoMenu = tamanio
            producto.descripcionProductoMenu = descripcion
            producto.precioProductoMenu = precio_decimal
            producto.idCategoriaProductoMenu = models.CategoriaProductoMenu.objects.get(idCategoriaProductoMenu=categoriaId)
            producto.save()
            return redirect(reverse('listar_productos_menu'))
        except models.CategoriaProductoMenu.DoesNotExist:
            categorias = models.CategoriaProductoMenu.objects.all()
            return render(request, 'registrar_producto_menu.html', {
                'categorias': categorias,
                'error': 'Categoría no válida. Por favor seleccione una categoría de la lista.',
                'nombre': nombre,
                'tamanio': tamanio,
                'descripcion': descripcion,
                'precio': precio
            })
        except Exception as e:
            categorias = models.CategoriaProductoMenu.objects.all()
            return render(request, 'registrar_producto_menu.html', {
                'categorias': categorias,
                'error': f'Error al registrar el producto: {str(e)}',
                'nombre': nombre,
                'tamanio': tamanio,
                'descripcion': descripcion,
                'precio': precio
            })
    
    elif request.method == "GET":
        categorias = models.CategoriaProductoMenu.objects.all()
        return render(request, 'registrar_producto_menu.html', {'categorias': categorias})

#CONTROLADOR PARA EDITAR PRODUCTOS PARA MENU
def editar_producto_menu(request, productoMenuId=None, invalid=None):
    if not productoMenuId or productoMenuId <1 or invalid:
        return redirect(reverse('listar_productos'))
    elif productoMenuId:
        producto = models.ProductoMenu.objects.filter(idProductoMenu=productoMenuId).first()
        if producto is None:
            return redirect(reverse('listar_productos'))
        if request.method == "POST":
            producto.nombreProductoMenu = request.POST.get("nombre-producto")
            producto.tamanioProductoMenu = request.POST.get("tamanio-producto")
            producto.descripcionProductoMenu = request.POST.get("descripcion-producto")
            producto.precioProductoMenu = request.POST.get("precio-producto")
            categoria = models.CategoriaProductoMenu.objects.filter(idCategoriaProductoMenu=request.POST.get("categoria-producto")).first()
            producto.idCategoriaProductoMenu = categoria
            producto.estaHabilitadoProductoMenu = True if request.POST.get("habilitado") else False
            producto.save()
            return redirect(reverse('editar_producto_menu', kwargs={'productoMenuId':productoMenuId}))
        elif request.method == "GET":
            categorias = models.CategoriaProductoMenu.objects.all()
            return render(request, 'editar_producto_menu.html' ,{'producto':producto, 'categorias':categorias})

#Controlador para ver productos del menu
def ver_producto_menu(request, productoMenuId=None):
    if not productoMenuId or not productoMenuId.isdigit() or int(productoMenuId) < 1:
        return redirect(reverse('listar_productos_menu'))
    else:
        producto = models.ProductoMenu.objects.filter(idProductoMenu=productoMenuId).first()
        if producto is None:
            return redirect(reverse('listar_productos_menu'))
        if request.method == "GET":
            return render(request, 'ver_producto_menu.html' ,{'producto':producto})

#Controlador para listar productos del menu
def listar_productos_menu(request):
    productos = models.ProductoMenu.objects.filter(estaHabilitadoProductoMenu=True)
    categorias = models.CategoriaProductoMenu.objects.all()
    return render(request, 'listar_menu.html' ,{'productos':productos,'categorias':categorias})

#Controlador para listar productos del menu deshabilitados
def listar_productos_deshabilitados_menu(request):
    productos = models.ProductoMenu.objects.filter(estaHabilitadoProductoMenu=False)
    categorias = models.CategoriaProductoMenu.objects.all()
    return render(request, 'listar_menu_deshabilitados.html' ,{'productos':productos,'categorias':categorias})

def cambiar_estado_producto_menu(request, productoMenuId=None):
    if not productoMenuId or not productoMenuId.isdigit() or int(productoMenuId) <1:
        return redirect(reverse('listar_productos_menu'))
    else:
        producto = models.ProductoMenu.objects.filter(idProductoMenu=productoMenuId).first()
        if producto is None:
            return redirect(reverse('listar_productos_menu'))
        if request.method == "POST":
            action = ast.literal_eval(request.POST.get("estaHabilitadoProductoMenu"))
            producto.estaHabilitadoProductoMenu = action
            producto.save()
            if action:
                url = 'listar_productos_deshabilitados_menu'
            else:
                url = 'listar_productos_menu'
            
            return redirect(reverse(url))
        if request.method == "GET":
            return redirect(reverse('listar_productos_menu'))

#CONTROLADOR PARA GESTIONAR CATEGORIAS
@login_required
@groups_required('Jefe')
def gestionar_categorias(request):
    if request.method == "POST":
        accion = request.POST.get('accion')
        
        if accion == 'crear':
            nombre = request.POST.get('nombre')
            if nombre:
                models.CategoriaProductoMenu.objects.create(
                    nombreCategoriaProductoMenu=nombre
                )
                url = reverse('gestionar_categorias')
                return redirect(f'{url}?exito=1')
        
        elif accion == 'editar':
            categoria_id = request.POST.get('categoria_id')
            nombre = request.POST.get('nombre')
            if categoria_id and nombre:
                categoria = models.CategoriaProductoMenu.objects.get(
                    idCategoriaProductoMenu=categoria_id
                )
                categoria.nombreCategoriaProductoMenu = nombre
                categoria.save()
                url = reverse('gestionar_categorias')
                return redirect(f'{url}?exito=2')
    
    categorias = models.CategoriaProductoMenu.objects.all().order_by('idCategoriaProductoMenu')
    return render(request, 'gestionar_categorias.html', {
        'categorias': categorias
    })

from django.shortcuts import redirect, render
from django.urls import reverse
from django.http import JsonResponse
from . import models

#API REST PARA PRODUCTOS DEL MENU
def api_producto_menu(request):
    if request.method == "GET":
        nombre = request.GET.get('nombre')
        categoria = request.GET.get('categoria')
        productos = list(models.ProductoMenu.objects.all().values())
        if nombre:
            productos = list(models.ProductoMenu.objects.filter(nombreProductoMenu__icontains=nombre).values())
        if categoria:
            productos = list(productos.filter(idCategoriaProductoMenu=categoria).values())
    return JsonResponse(productos, safe=False)

#CONTROLADOR PARA REGISTRO DE PRODUCTOS PARA MENU
def registrar_producto_menu(request):
    if request.method == "POST":
        print(request.POST)
        producto = models.ProductoMenu()
        producto.nombreProductoMenu = request.POST.get("nombre-producto")
        producto.tamanioProductoMenu = request.POST.get("tamanio-producto")
        producto.descripcionProductoMenu = request.POST.get("descripcion-producto")
        producto.precioProductoMenu = request.POST.get("precio-producto")
        categoriaId =request.POST.get("categoria-producto")
        print(categoriaId)
        producto.idCategoriaProductoMenu = models.CategoriaProductoMenu.objects.get(idCategoriaProductoMenu=categoriaId) 
        producto.save()
        return redirect(reverse('listar_productos_menu'))
    elif request.method == "GET":
        categorias = models.CategoriaProductoMenu.objects.all()
        return render(request, 'registrar_producto_menu.html' ,{'categorias':categorias})

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
        return redirect(reverse('listar_productos'))
    else:
        producto = models.ProductoMenu.objects.filter(idProductoMenu=productoMenuId).first()
        if producto is None:
            return redirect(reverse('listar_productos'))
        if request.method == "GET":
            return render(request, 'ver_producto_menu.html' ,{'producto':producto})

#Controlador para listar productos del menu
def listar_productos_menu(request):
    productos = models.ProductoMenu.objects.all()
    categorias = models.CategoriaProductoMenu.objects.all()
    return render(request, 'listar_menu.html' ,{'productos':productos,'categorias':categorias})
        
            
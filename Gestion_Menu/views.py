from django.shortcuts import redirect, render
from django.urls import reverse
from . import models

# Create your views here.

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
        return redirect(reverse('registrar_producto_menu'))
    elif request.method == "GET":
        categorias = models.CategoriaProductoMenu.objects.all()
        return render(request, 'registrar_producto_menu.html' ,{'categorias':categorias})
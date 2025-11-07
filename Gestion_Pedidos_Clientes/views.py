from django.shortcuts import render
from Gestion_Menu.models import CategoriaProductoMenu, ProductoMenu
from django.db.models import Prefetch

# Create your views here.

def crear_pedido(request):
    if request.method == 'GET':
        categorias_con_productos = (CategoriaProductoMenu.objects.filter(
        productomenu__estaHabilitadoProductoMenu=True).distinct().prefetch_related(
        Prefetch('productomenu_set',queryset=ProductoMenu.objects.filter(estaHabilitadoProductoMenu=True))))
    return render(request, 'crear_pedido.html', {'categorias_con_productos':categorias_con_productos})

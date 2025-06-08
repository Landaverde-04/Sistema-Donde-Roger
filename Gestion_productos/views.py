from django.shortcuts import render
#from .models import Producto
from django.shortcuts import render,redirect


# Create your views here.
# viem de registrar un producto
def registrar_producto(request):
    

    return render(request, 'registrar_producto.html')
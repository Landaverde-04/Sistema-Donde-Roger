from django.shortcuts import render
#from .models import Producto
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
# viem de registrar un producto

@login_required
def registrar_producto(request):
    

    return render(request, 'registrar_producto.html')
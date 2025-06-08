from django.shortcuts import render
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required
def registrar_proveedor(request):
    return render(request, 'registrar_proveedor.html')


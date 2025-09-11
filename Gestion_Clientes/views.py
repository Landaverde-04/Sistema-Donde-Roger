from django.shortcuts import render

# Create your views here.
def registrar_cliente(request):
    return render(request, 'registrar_cliente.html')
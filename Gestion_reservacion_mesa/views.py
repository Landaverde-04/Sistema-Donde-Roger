from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required


# Create your views here.

@login_required
def crear_reserva(request):
    if request.method == 'POST':
        # Lógica para crear la reserva
        return redirect('ver_reservas')
    return render(request, 'crear_reserva.html')

@login_required
def ver_reservas(request):
    
    return render(request, 'ver_reservas.html')

@login_required
def cancelar_reserva(request):
    if request.method == 'POST':
        # Lógica para cancelar la reserva
        return redirect('ver_reservas')
    return render(request, 'cancelar_reserva.html')

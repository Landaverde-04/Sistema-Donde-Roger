
from django.shortcuts import render, redirect
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from empleado.models import Empleado  # Ajusta el import a tu app
from .models import Usuario  # Ajusta a tu modelo extendido

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('/inventario/ver_inventario')
        else:
            messages.error(request, 'Credenciales inválidas')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

User = get_user_model()

def is_jefe(user):
    return user.groups.filter(name='Jefe').exists()

@login_required
#@user_passes_test(is_jefe)
def crear_usuario_view(request):
    empleados = Empleado.objects.filter(estaHabilitadoEmpleado=True)
    grupos = Group.objects.all()

    if request.method == 'POST':
        empleado_id = request.POST.get('empleado')
        username = request.POST.get('username')
        password = request.POST.get('password')
        grupo_id = request.POST.get('grupo')

        empleado = Empleado.objects.get(idEmpleado=empleado_id)
        grupo = Group.objects.get(id=grupo_id)
        
        user = User.objects.create_user(username=username, password=password)
        user.idEmpleado = empleado  # Ajusta según tu modelo
        user.save()
        user.groups.add(grupo)
        return redirect('dashboard')  # Cambia al nombre correcto

    return render(request, 'crear_usuario.html', {
        'empleados': empleados,
        'grupos': grupos,
    })


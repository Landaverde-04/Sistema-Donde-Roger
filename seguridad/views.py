
from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib import messages
from django.contrib.auth import get_user_model
from empleado.models import Empleado  # Ajusta el import a tu app
from .models import Usuario # Ajusta a tu modelo extendido
from .decoradores import groups_required

User = get_user_model()

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


def is_jefe(user):
    return user.groups.filter(name='Jefe').exists()

@login_required
@groups_required('Jefe')
#@user_passes_test(is_jefe)
def crear_usuario_view(request):
    empleados = Empleado.objects.filter(estaHabilitadoEmpleado=True)
    grupos = Group.objects.all()

    if request.method == 'POST':
        empleado_id = request.POST.get('empleado')
        username = request.POST.get('username')
        password = request.POST.get('password')
        grupo_id = request.POST.get('grupo')
        email = request.POST.get('email') 

        empleado = Empleado.objects.get(idEmpleado=empleado_id)
        grupo = Group.objects.get(id=grupo_id)
        
        user = User.objects.create_user(username=username, password=password,email=email)
        user.idEmpleado = empleado  # Ajusta según tu modelo
        user.save()
        messages.success(request, "Usuario creado exitosamente.")
        user.groups.add(grupo)
        return redirect('usuario_lista')  

    return render(request, 'crear_usuario.html', {
        'empleados': empleados,
        'grupos': grupos,
    })

@login_required
@groups_required('Jefe')
def usuario_lista_view(request):
    usuarios = User.objects.all()
    return render(request, 'usuario_lista.html', {'usuarios': usuarios})

@login_required
@groups_required('Jefe')
def ver_usuario_view(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    return render(request, 'ver_usuario.html', {'usuario': usuario})

@login_required
@groups_required('Jefe')
def modificar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    empleados = Empleado.objects.filter(estaHabilitadoEmpleado=True)
    grupos = Group.objects.all()

    if request.method == 'POST':
        empleado_id = request.POST.get('empleado')
        grupo_id = request.POST.get('grupo')
        username = request.POST.get('username')
        email = request.POST.get('email')   
        password = request.POST.get('password')


        empleado = Empleado.objects.get(idEmpleado=empleado_id)
        grupo = Group.objects.get(id=grupo_id)
        usuario.username = username
        usuario.idEmpleado = empleado
        usuario.email = email
        if password:
            usuario.set_password(password)
        usuario.groups.clear()
        usuario.groups.add(grupo)
        usuario.save()
        messages.success(request, "Usuario modificado exitosamente.")
        return redirect('usuario_lista')
    
    return render(request, 'modificar_usuario.html', {
        'usuario': usuario,
        'empleados': empleados,
        'grupos': grupos,
    })

@login_required
@groups_required('Jefe')
def eliminar_usuario_view(request, usuario_id):
    usuario = get_object_or_404(User, id=usuario_id)
    if request.method == 'POST':
        usuario.delete()
        messages.success(request, "Usuario eliminado exitosamente.")
        return redirect('usuario_lista')
    return render(request, 'eliminar_usuario.html', {'usuario': usuario})

from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Empleado
from django.contrib import messages


def registrar_empleado(request):
    if request.method == 'POST':
        # Recoger los datos enviados a través del POST (sin incluir idEmpleado)
        nombresEmpleado = request.POST.get('nombresEmpleado')
        apellidosEmpleado = request.POST.get('apellidosEmpleado')
        duiEmpleado = request.POST.get('duiEmpleado')
        fechaNacimientoEmpleado = request.POST.get('fechaNacimientoEmpleado')
        telEmpleado = request.POST.get('telEmpleado')
        telEmergenciaEmpleado = request.POST.get('telEmergenciaEmpleado')
        salarioEmpleado = request.POST.get('salarioEmpleado')
        experienciaLaboralEmpleado = request.POST.get('experienciaLaboralEmpleado')
        fechaContratacionEmpleado = request.POST.get('fechaContratacionEmpleado')
        direccionEmpleado = request.POST.get('direccionEmpleado')
        contratoEmpleado = request.FILES.get('contratoEmpleado')  # Recoger el archivo subido

        try:
            # Crear un nuevo empleado sin necesidad de incluir idEmpleado
            empleado = Empleado.objects.create(
                nombresEmpleado=nombresEmpleado,
                apellidosEmpleado=apellidosEmpleado,
                duiEmpleado=duiEmpleado,
                fechaNacimientoEmpleado=fechaNacimientoEmpleado,
                telEmpleado=telEmpleado,
                telEmergenciaEmpleado=telEmergenciaEmpleado,
                salarioEmpleado=salarioEmpleado,
                experienciaLaboralEmpleado=experienciaLaboralEmpleado,
                fechaContratacionEmpleado=fechaContratacionEmpleado,
                 direccionEmpleado=direccionEmpleado,
                contratoEmpleado=contratoEmpleado,
                estaHabilitadoEmpleado= True
            )
            messages.success(request, "Empleado registrado con éxito")
            return redirect('empleado_lista')  # Redirige a la lista de empleados o donde prefieras
        except Exception as e:
            return HttpResponse(f"Error al registrar empleado: {e}", status=400)

    return render(request, 'registrar_empleado.html')

def empleado_lista(request):
    empleados = Empleado.objects.all()
    return render(request, 'empleado_lista.html', {'empleados': empleados})


def modificar_empleado(request, idEmpleado):
    empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
    if request.method == 'POST':
        empleado.nombresEmpleado = request.POST.get('nombresEmpleado')
        empleado.apellidosEmpleado = request.POST.get('apellidosEmpleado')
        empleado.duiEmpleado = request.POST.get('duiEmpleado')
        empleado.fechaNacimientoEmpleado = request.POST.get('fechaNacimientoEmpleado')
        empleado.telEmpleado = request.POST.get('telEmpleado')
        empleado.direccionEmpleado = request.POST.get('direccionEmpleado')
        empleado.telEmergenciaEmpleado = request.POST.get('telEmergenciaEmpleado')
        empleado.salarioEmpleado = request.POST.get('salarioEmpleado')
        empleado.experienciaLaboralEmpleado = request.POST.get('experienciaLaboralEmpleado')
        empleado.fechaContratacionEmpleado = request.POST.get('fechaContratacionEmpleado')
        # Si sube nuevo contrato:
        if request.FILES.get('contratoEmpleado'):
            empleado.contratoEmpleado = request.FILES.get('contratoEmpleado')
        empleado.save()
        messages.success(request, "Actualización realizada con éxito")
        return redirect('empleado_lista')
    return render(request, 'modificar_empleado.html', {'empleado': empleado})

def ver_empleado(request, idEmpleado):
    empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
    return render(request, 'ver_empleado.html', {'empleado': empleado})


def eliminar_empleado(request, idEmpleado):
    empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
    if request.method == 'POST':
        empleado.delete()
        messages.success(request, "Empleado eliminado exitosamente.")
        return redirect('empleado_lista')
    # Si por accidente alguien entra a GET, simplemente redirige:
    return redirect('empleado_lista')
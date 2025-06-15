from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Empleado

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
        contratoEmpleado = request.FILES.get('contratoEmpleado')  # Recoger el archivo subido
        estaHabilitadoEmpleado = request.POST.get('estaHabilitadoEmpleado') == 'on'

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
                contratoEmpleado=contratoEmpleado,
                estaHabilitadoEmpleado=estaHabilitadoEmpleado
            )
            return redirect('empleado_lista')  # Redirige a la lista de empleados o donde prefieras
        except Exception as e:
            return HttpResponse(f"Error al registrar empleado: {e}", status=400)

    return render(request, 'registrar_empleado.html')

def empleado_lista(request):
    empleados = Empleado.objects.all()  # Obtener todos los empleados
    return render(request, 'empleado_lista.html', {'empleados': empleados})

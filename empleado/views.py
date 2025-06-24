from django.shortcuts import render, redirect,get_object_or_404
from django.http import HttpResponse
from .models import Empleado
from django.contrib import messages
from .models import Empleado, Asistencia
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required
from django.core.paginator import Paginator
from django.db.models import Q



@login_required
@groups_required('Jefe')
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
            empleado.save()
            messages.success(request, "Empleado registrado con éxito", extra_tags='empleado')
            return redirect('empleado_lista',)  
        except Exception as e:
            return HttpResponse(f"Error al registrar empleado: {e}", status=400)

    return render(request, 'registrar_empleado.html')

#def empleado_lista(request):
 #   busqueda = request.GET.get('busqueda', '')
  #  if busqueda:
   #     empleados = Empleado.objects.filter(
    #        Q(nombresEmpleado__icontains=busqueda) |
     #       Q(apellidosEmpleado__icontains=busqueda)
      #  )
    #else:
     #   empleados = Empleado.objects.all()
    #return render(request, 'empleado_lista.html', {'empleados': empleados})
    

@login_required
@groups_required('Jefe')
def empleado_lista(request):
    busqueda = request.GET.get('busqueda', '')
    empleados_query = Empleado.objects.filter(estaHabilitadoEmpleado=True).order_by('idEmpleado')

    if busqueda:
        empleados_query = empleados_query.filter(
            Q(nombresEmpleado__icontains=busqueda) |
            Q(apellidosEmpleado__icontains=busqueda)
        )

    paginator = Paginator(empleados_query, 10)  
    page_number = request.GET.get('page')
    empleados_paginacion = paginator.get_page(page_number)

    return render(request, 'empleado_lista.html', {
        'empleados_paginacion': empleados_paginacion,
        'busqueda': busqueda,
    })


@login_required
@groups_required('Jefe')
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
        messages.success(request, "Actualización realizada con éxito", extra_tags='empleado')
        return redirect('empleado_lista')
    return render(request, 'modificar_empleado.html', {'empleado': empleado})


@login_required
@groups_required('Jefe')
def ver_empleado(request, idEmpleado):
    empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
    return render(request, 'ver_empleado.html', {'empleado': empleado})


@login_required
@groups_required('Jefe')
def eliminar_empleado(request, idEmpleado):
    empleado = get_object_or_404(Empleado, idEmpleado=idEmpleado)
    if request.method == 'POST':
        empleado.estaHabilitadoEmpleado = False  # Cambia a inhabilitado
        empleado.save()  # Guarda el cambio en la BD
        messages.success(request, "Empleado inhabilitado exitosamente.", extra_tags='empleado')
        return redirect('empleado_lista')
    # Si alguien entra a GET, simplemente redirige:
    return redirect('empleado_lista')


#Vista de asistencia
@login_required
def marcar_asistencia(request):
    usuario = request.user
    ahora = timezone.now()#aca guardamos la fecha y hora actual, en este 
    #caso es local porque USE_TZ= False
    fecha_hoy = ahora.date()#guarda solo fecha
    hora_actual = ahora.time()#guarda solo hora

    # Buscar si hay una asistencia activa (sin hora de salida)
    asistencia_abierta = Asistencia.objects.filter(
        usuario=usuario,
        horaSalida__isnull=True #con esta variable preguntamos con la sintaxis
        #de django si la variable está vacía o no, la sintaxis "__isnull"
    ).order_by('-fecha', '-horaEntrada').first()#ordenamos por orden descendente
    #por eso tiene el "-" antes de fecha y hora entrada

    mensaje = ""#declaramos la varibale que almacena los mensajes

    if request.method == 'POST':#cuando el usuario envia el formulario
        if 'entrada' in request.POST:
            if asistencia_abierta:#si asistencia es abierta entonces no puede marcar otra entrada
                mensaje = "Ya tienes una entrada activa. Debes marcar salida antes."
            else:#sino pues hace la entrada
                Asistencia.objects.create(
                    usuario=usuario,
                    fecha=fecha_hoy,
                    horaEntrada=hora_actual
                )
                mensaje = "Entrada registrada correctamente."

        elif 'salida' in request.POST:#si se manda formulario de salida
            if asistencia_abierta:#y asistencia está abierta
                asistencia_abierta.horaSalida = hora_actual
                asistencia_abierta.save()#se guarda la salida
                mensaje = "Salida registrada correctamente."
            else:#sino no guarda salida
                mensaje = "No tienes una entrada activa. Marca entrada primero."

    return render(request, 'marcar_asistencia.html', {
        'mensaje': mensaje,#mandamos el mensaje
        'asistencia_abierta': asistencia_abierta,#mandamos la variable de asistencia
        'empleado': usuario.idEmpleado,  # Para mostrar el nombre
    })

@login_required
@groups_required('Jefe')
def historial_asistencia(request):
    nombre = request.GET.get('nombre', '').strip()
    fecha = request.GET.get('fecha', '').strip()

    asistencias = Asistencia.objects.select_related('usuario__idEmpleado').order_by(
        'usuario__idEmpleado__nombresEmpleado', '-fecha'
    )

    if nombre:
        asistencias = asistencias.filter(
            Q(usuario__idEmpleado__nombresEmpleado__icontains=nombre) |
            Q(usuario__idEmpleado__apellidosEmpleado__icontains=nombre)
        )
    if fecha:
        asistencias = asistencias.filter(fecha=fecha)
        

    paginator = Paginator(asistencias, 10)  # 10 registros por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'nombre': nombre,
        'fecha': fecha,
    }
    return render(request, 'historial_asistencia.html', context)

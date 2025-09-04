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
from django.urls import reverse



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
    # Obtenemos el usuario que está logueado
    usuario = request.user

    # Obtenemos la fecha y hora actuales del sistema
    ahora = timezone.now()  # timezone.now() devuelve la fecha y hora actual (local si USE_TZ=False)
    fecha_hoy = ahora.date()  # solo la fecha de hoy
    hora_actual = ahora.time()  # solo la hora actual

    # Buscamos si hay una asistencia abierta para este usuario (sin hora de salida)
    # .filter(...) busca todas las asistencias del usuario que aún no tengan horaSalida
    # .order_by('-fecha', '-horaEntrada') ordena de más reciente a más antigua
    # .first() obtiene solo la más reciente o None si no hay ninguna
    asistencia_abierta = Asistencia.objects.filter(
        usuario=usuario,
        horaSalida__isnull=True
    ).order_by('-fecha', '-horaEntrada').first()

    # Verificamos si se envió un formulario mediante POST
    if request.method == 'POST':

        # Si el formulario enviado es de entrada
        if 'entrada' in request.POST:
            if not asistencia_abierta:
                # No hay asistencia abierta → creamos un registro de entrada
                Asistencia.objects.create(
                    usuario=usuario,
                    fecha=fecha_hoy,
                    horaEntrada=hora_actual
                )
                # Guardamos un mensaje temporal en la sesión del usuario
                # Este mensaje se mostrará solo una vez tras el redirect
                request.session['mensaje'] = "Entrada registrada correctamente."
            else:
                # Si ya había una entrada activa, no se puede registrar otra
                request.session['mensaje'] = "Ya tienes una entrada activa."

        # Si el formulario enviado es de salida
        elif 'salida' in request.POST:
            if asistencia_abierta:
                # Si hay una asistencia abierta, guardamos la hora de salida
                asistencia_abierta.horaSalida = hora_actual
                asistencia_abierta.save()
                # Guardamos un mensaje temporal en la sesión
                request.session['mensaje'] = "Salida registrada correctamente."
            else:
                # No hay entrada activa → no se puede registrar salida
                request.session['mensaje'] = "No tienes una entrada activa."

        # Después de procesar el POST, hacemos un redirect a la misma vista
        # Esto evita que al refrescar la página se vuelva a enviar el formulario
        # Patroon PRG: Post → Redirect → Get
        return redirect(reverse('marcar_asistencia'))

    # Si es GET (o después del redirect):
    # Recuperamos el mensaje que guardamos en la sesión y lo eliminamos
    # pop() devuelve el valor y elimina la clave, así el mensaje solo se muestra una vez
    # Si no hay mensaje, devuelve None
    mensaje = request.session.pop('mensaje', None)

    # Renderizamos la plantilla con los datos necesarios
    return render(request, 'marcar_asistencia.html', {
        'mensaje': mensaje,  # mensaje a mostrar en el template (si hay)
        'asistencia_abierta': asistencia_abierta,  # estado de asistencia para cambiar el botón
        'empleado': usuario.idEmpleado,  # información del empleado para mostrar en la interfaz
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

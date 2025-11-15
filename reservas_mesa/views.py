from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import ReservaMesa, Mesa
from .models import ReservaMesa
from .forms import ReservaMesaForm
from django.urls import reverse
from datetime import timedelta


# Decorador local: groups_required('Jefe', 'Gerente', ...)
def groups_required(*group_names):
    """
    Permite acceso sólo a usuarios autenticados que pertenezcan
    a alguno de los grupos indicados o sean superusuarios.
    """
    def decorator(view_func):
        @user_passes_test(
            lambda u: u.is_authenticated and (
                u.is_superuser or u.groups.filter(name__in=group_names).exists()
            )
        )
        def _wrapped_view(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# HU-32: Crear reservación de mesa
@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def crear_reserva_mesa(request):
    mesa_id = request.GET.get('mesa')

    if request.method == 'POST':
        form = ReservaMesaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.creado_por = request.user
            reserva.save()
            messages.success(request, "Reservación creada correctamente.")
            return redirect('listar_reservas_hoy')
    else:
        initial = {}
        if mesa_id:
            initial['mesa'] = mesa_id
        form = ReservaMesaForm(initial=initial)

    return render(request, 'reservas_mesa/crear_reserva.html', {'form': form})


# HU-34: Ver reservas de mesa del día actual
@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def listar_reservas_hoy(request):
    ahora = timezone.now()

    # --- 1) ACTUALIZAR RESERVAS VENCIDAS A FINALIZADA ---
    reservas_vencidas = ReservaMesa.objects.filter(
        fecha_hora__lt=ahora - timedelta(minutes=45),
        estado__in=['PENDIENTE', 'CONFIRMADA']
    )
    for r in reservas_vencidas:
        r.actualizar_estado_por_tiempo(minutos=45)

    # --- 2) OBTENER RESERVAS SOLO DEL DÍA ACTUAL ---
    inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
    fin_dia = inicio_dia + timedelta(days=1)

    qs = ReservaMesa.objects.filter(
        fecha_hora__gte=inicio_dia,
        fecha_hora__lt=fin_dia,
    )

    # --- 3) ORDENAR: PRIMERO FUTURAS → LUEGO PASADAS ---
    futuras = qs.filter(fecha_hora__gte=ahora).order_by('fecha_hora')
    pasadas = qs.filter(fecha_hora__lt=ahora).order_by('fecha_hora')

    reservas = list(futuras) + list(pasadas)

    # --- 4) CONTAR POR ESTADOS ---
    total_pendientes = qs.filter(estado='PENDIENTE').count()
    total_confirmadas = qs.filter(estado='CONFIRMADA').count()
    total_canceladas = qs.filter(estado='CANCELADA').count()
    total_finalizadas = qs.filter(estado='FINALIZADA').count()

    return render(request, 'reservas_mesa/listar_hoy.html', {
        'reservas': reservas,
        'total_pendientes': total_pendientes,
        'total_confirmadas': total_confirmadas,
        'total_canceladas': total_canceladas,
        'total_finalizadas': total_finalizadas,
    })

# HU-35: Ver / modificar una reservación
@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def ver_reserva_mesa(request, pk):
    reserva = get_object_or_404(ReservaMesa, pk=pk)

    if request.method == 'POST':
        form = ReservaMesaForm(request.POST, instance=reserva)
        if form.is_valid():
            form.save()
            messages.success(request, "Reservación actualizada correctamente.")
            return redirect('listar_reservas_hoy')
    else:
        form = ReservaMesaForm(instance=reserva)

    return render(request, 'reservas_mesa/ver_reserva.html', {
        'reserva': reserva,
        'form': form,
    })


# HU-33: Cancelar reservación
@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def cancelar_reserva_mesa(request, pk):
    reserva = get_object_or_404(ReservaMesa, pk=pk)

    if request.method == 'POST':
        # AC1: se pidió confirmación en el template
        reserva.estado = 'CANCELADA'
        reserva.save()
        messages.success(request, "La reservación ha sido cancelada.")
        return redirect('listar_reservas_hoy')

    return render(request, 'reservas_mesa/confirmar_cancelacion.html', {
        'reserva': reserva,
    })


# HU-36: Historial de reservas
@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def historial_reservas_mesa(request):
    ahora = timezone.now()

    # 1) Actualizar reservas vencidas a FINALIZADA
    reservas_vencidas = ReservaMesa.objects.filter(
        fecha_hora__lt=ahora - timedelta(minutes=45),
        estado__in=['PENDIENTE', 'CONFIRMADA']
    )
    for r in reservas_vencidas:
        r.actualizar_estado_por_tiempo(minutos=45)

    # 2) Ya construimos el queryset para mostrar
    qs = ReservaMesa.objects.filter(fecha_hora__lt=ahora)

    # Filtros por fecha y nombre
    fecha = request.GET.get('fecha')
    nombre = request.GET.get('nombre')

    if fecha:
        qs = qs.filter(fecha_hora__date=fecha)
    if nombre:
        qs = qs.filter(nombre_contacto__icontains=nombre)

    try:
        limite = int(request.GET.get('limite', 10))
    except ValueError:
        limite = 10
    limite = max(1, min(limite, 30))

    reservas = qs.order_by('-fecha_hora')[:limite]

    return render(request, 'reservas_mesa/historial.html', {
        'reservas': reservas,
        'limite': limite,
        'fecha': fecha,
        'nombre': nombre,
    })

@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def mapa_mesas(request):
    mesas = Mesa.objects.all().order_by('numero')

    # adjuntamos el estado calculado a cada mesa
    for mesa in mesas:
        mesa.estado_actual = mesa.get_estado_actual()

    return render(request, 'reservas_mesa/mapa_mesas.html', {
        'mesas': mesas,
    })


@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def detalle_mesa(request, mesa_id):
    """
    Si la mesa está LIBRE → redirige a crear_reserva_mesa con la mesa preseleccionada.
    Si está RESERVADA u OCUPADA → muestra la reserva asociada con opciones.
    """
    mesa = get_object_or_404(Mesa, pk=mesa_id)
    estado = mesa.get_estado_actual()
    reserva = mesa.get_reserva_actual()

    # Si no hay ninguna reserva hoy o la mesa está libre → crear nueva reserva
    if estado == 'LIBRE' or reserva is None:
        url = reverse('crear_reserva_mesa')
        return redirect(f'{url}?mesa={mesa.id}')

    # Si hay reserva asociada (RESERVADA u OCUPADA), mostramos detalles
    contexto = {
        'mesa': mesa,
        'estado': estado,
        'reserva': reserva,
    }
    return render(request, 'reservas_mesa/detalle_mesa.html', contexto)

@login_required
@groups_required('Jefe', 'Gerente', 'Colaborador')
def eliminar_reserva_mesa(request, pk):
    reserva = get_object_or_404(ReservaMesa, pk=pk)

    if request.method == 'POST':
        mesa_num = reserva.mesa.numero
        reserva.delete()
        messages.success(
            request,
            f"La reservación de la mesa {mesa_num} ha sido eliminada permanentemente."
        )
        return redirect('listar_reservas_hoy')

    return render(request, 'reservas_mesa/confirmar_eliminar.html', {
        'reserva': reserva
    })
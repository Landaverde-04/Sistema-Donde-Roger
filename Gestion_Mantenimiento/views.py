# Gestion_Mantenimiento/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q

from Gestion_Maquinaria.models import Maquinaria
from .models import Mantenimiento
from seguridad.decoradores import groups_required  # usa tu decorador real

VALID_MIMES = {'image/jpeg', 'image/png'}

def _maqs():
    return Maquinaria.objects.all().order_by('idMaquinaria')

# ---------- LISTA ----------
@login_required
@groups_required('Jefe')
def lista_mantenimiento(request):
    busqueda = request.GET.get('busqueda', '').strip()
    maq_id = request.GET.get('maquinaria', '')

    qs = Mantenimiento.objects.select_related('maquinaria').all()
    if maq_id:
        qs = qs.filter(maquinaria_id=maq_id)
    if busqueda:
        qs = qs.filter(
            Q(nombreTecnico__icontains=busqueda) |
            Q(maquinaria__nombreMaquinaria__icontains=busqueda) |
            Q(maquinaria__marcaMaquinaria__icontains=busqueda)
        )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lista_mantenimiento.html', {
        'mantenimientos': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'busqueda': busqueda,
        'maquinaria_sel': maq_id,
        'maquinarias': _maqs(),
    })

# ---------- REGISTRAR ----------
@login_required
@groups_required('Jefe')
def registrar_mantenimiento(request):
    if request.method == 'POST':
        form_data = {
            'maquinaria': request.POST.get('maquinaria'),
            'fechaMantenimiento': request.POST.get('fechaMantenimiento'),
            'esCorrectivo': request.POST.get('esCorrectivo') == 'on',
            'nombreTecnico': request.POST.get('nombreTecnico'),
            'observaciones': request.POST.get('observaciones') or '',
        }
        files_data = {
            'fotoAntesURL': request.FILES.get('fotoAntesURL'),
            'fotoDespuesURL': request.FILES.get('fotoDespuesURL'),
            'fotoFacturaURL': request.FILES.get('fotoFacturaURL'),
        }

        # Validación básica
        errors = []
        if not form_data['maquinaria']:
            errors.append("Debe seleccionar una maquinaria.")
        if not form_data['fechaMantenimiento']:
            errors.append("La fecha es obligatoria.")
        if not form_data['nombreTecnico']:
            errors.append("El nombre del técnico es obligatorio.")
        for f in files_data.values():
            if f and f.content_type not in VALID_MIMES:
                errors.append("Solo se permiten imágenes PNG o JPG.")

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'registrar_mantenimiento.html', {
                'maquinarias': _maqs(),
                'form': form_data
            })

        try:
            maquinaria = get_object_or_404(Maquinaria, idMaquinaria=form_data['maquinaria'])
            Mantenimiento.objects.create(
                maquinaria=maquinaria,
                fechaMantenimiento=form_data['fechaMantenimiento'],
                esCorrectivo=form_data['esCorrectivo'],
                nombreTecnico=form_data['nombreTecnico'],
                observaciones=form_data['observaciones'],
                fotoAntesURL=files_data['fotoAntesURL'],
                fotoDespuesURL=files_data['fotoDespuesURL'],
                fotoFacturaURL=files_data['fotoFacturaURL'],
            )
            messages.success(request, "Mantenimiento registrado.")
            return redirect('lista_mantenimiento')
        except Exception as e:
            messages.error(request, f"No se pudo guardar: {e}")
            return render(request, 'registrar_mantenimiento.html', {
                'maquinarias': _maqs(),
                'form': form_data
            })

    # GET
    return render(request, 'registrar_mantenimiento.html', {
        'maquinarias': _maqs()
    })

# ---------- VER ----------
@login_required
@groups_required('Jefe')
def ver_mantenimiento(request, idMantenimiento):
    mant = get_object_or_404(Mantenimiento, idMantenimiento=idMantenimiento)
    return render(request, 'ver_mantenimiento.html', {'mantenimiento': mant})

# ---------- MODIFICAR ----------
@login_required
@groups_required('Jefe')
def modificar_mantenimiento(request, idMantenimiento):
    mant = get_object_or_404(Mantenimiento, idMantenimiento=idMantenimiento)

    if request.method == 'POST':
        form_data = {
            'maquinaria': request.POST.get('maquinaria'),
            'fechaMantenimiento': request.POST.get('fechaMantenimiento'),
            'esCorrectivo': request.POST.get('esCorrectivo') == 'on',
            'nombreTecnico': request.POST.get('nombreTecnico'),
            'observaciones': request.POST.get('observaciones') or '',
        }
        files_data = {
            'fotoAntesURL': request.FILES.get('fotoAntesURL'),
            'fotoDespuesURL': request.FILES.get('fotoDespuesURL'),
            'fotoFacturaURL': request.FILES.get('fotoFacturaURL'),
        }

        errors = []
        if not form_data['maquinaria']:
            errors.append("Debe seleccionar una maquinaria.")
        if not form_data['fechaMantenimiento']:
            errors.append("La fecha es obligatoria.")
        if not form_data['nombreTecnico']:
            errors.append("El nombre del técnico es obligatorio.")
        for f in files_data.values():
            if f and f.content_type not in VALID_MIMES:
                errors.append("Solo se permiten imágenes PNG o JPG.")

        if errors:
            for e in errors:
                messages.error(request, e)
            return render(request, 'modificar_mantenimiento.html', {
                'mantenimiento': mant,
                'maquinarias': _maqs(),
                'form': form_data
            })

        try:
            mant.maquinaria = get_object_or_404(Maquinaria, idMaquinaria=form_data['maquinaria'])
            mant.fechaMantenimiento = form_data['fechaMantenimiento']
            mant.esCorrectivo = form_data['esCorrectivo']
            mant.nombreTecnico = form_data['nombreTecnico']
            mant.observaciones = form_data['observaciones']

            if files_data['fotoAntesURL']:
                mant.fotoAntesURL = files_data['fotoAntesURL']
            if files_data['fotoDespuesURL']:
                mant.fotoDespuesURL = files_data['fotoDespuesURL']
            if files_data['fotoFacturaURL']:
                mant.fotoFacturaURL = files_data['fotoFacturaURL']

            mant.save()
            messages.success(request, "Mantenimiento actualizado.")
            return redirect('lista_mantenimiento')
        except Exception as e:
            messages.error(request, f"No se pudo actualizar: {e}")
            return render(request, 'modificar_mantenimiento.html', {
                'mantenimiento': mant,
                'maquinarias': _maqs(),
                'form': form_data
            })

    # GET
    return render(request, 'modificar_mantenimiento.html', {
        'mantenimiento': mant,
        'maquinarias': _maqs()
    })

# ---------- ELIMINAR (físico) ----------
@login_required
@groups_required('Jefe')
def eliminar_mantenimiento(request, idMantenimiento):
    mant = get_object_or_404(Mantenimiento, idMantenimiento=idMantenimiento)
    mant.delete()
    messages.success(request, "Mantenimiento eliminado definitivamente.")
    return redirect('lista_mantenimiento')


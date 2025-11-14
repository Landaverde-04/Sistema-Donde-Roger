from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required
from django.core.paginator import Paginator
from django.db.models import Q


from .models import Maquinaria



@login_required
@groups_required('Jefe')
def registrar_maquinaria(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombreMaquinaria')
        fecha_compra = request.POST.get('fechaCompraMaquinaria')
        marca = request.POST.get('marcaMaquinaria')

        try:
            Maquinaria.objects.create(
                nombreMaquinaria=nombre,
                fechaCompraMaquinaria=fecha_compra,
                marcaMaquinaria=marca,
                estaHabilitadaMaquinaria=True
            )
            messages.success(request, "Maquinaria registrada con éxito.", extra_tags='maquinaria')
            return redirect('lista_maquinaria')
        except Exception as e:
            messages.error(request, f"Error al registrar: {e}")
    return render(request, 'registrar_maquinaria.html')


@login_required
@groups_required('Jefe')
def lista_maquinaria(request):
    busqueda = request.GET.get('busqueda', '').strip()
    qs = Maquinaria.objects.filter(estaHabilitadaMaquinaria=True).order_by('idMaquinaria')
    if busqueda:
        qs = qs.filter(
            Q(nombreMaquinaria__icontains=busqueda) |
            Q(marcaMaquinaria__icontains=busqueda)
        )

    paginator = Paginator(qs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'lista_maquinaria.html', {
        'maquinarias': page_obj,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'busqueda': busqueda,
    })


@login_required
@groups_required('Jefe')
def ver_maquinaria(request, idMaquinaria):
    maquinaria = get_object_or_404(Maquinaria, idMaquinaria=idMaquinaria)
    return render(request, 'ver_maquinaria.html', {'maquinaria': maquinaria})


@login_required
@groups_required('Jefe')
def modificar_maquinaria(request, idMaquinaria):
    maquinaria = get_object_or_404(Maquinaria, idMaquinaria=idMaquinaria)
    if request.method == 'POST':
        maquinaria.nombreMaquinaria = request.POST.get('nombreMaquinaria')
        maquinaria.fechaCompraMaquinaria = request.POST.get('fechaCompraMaquinaria')
        maquinaria.marcaMaquinaria = request.POST.get('marcaMaquinaria')
        maquinaria.save()
        messages.success(request, "Actualización realizada con éxito.", extra_tags='maquinaria')
        return redirect('lista_maquinaria')

    return render(request, 'modificar_maquinaria.html', {'maquinaria': maquinaria})



@login_required
@groups_required('Jefe')
def eliminar_maquinaria(request, idMaquinaria):
    maquinaria = get_object_or_404(Maquinaria, idMaquinaria=idMaquinaria)
    if request.method == 'POST':
        maquinaria.delete()  
        messages.success(request, "Maquinaria eliminada definitivamente.", extra_tags='maquinaria')
        return redirect('lista_maquinaria')
    return redirect('maquinaria_lista')


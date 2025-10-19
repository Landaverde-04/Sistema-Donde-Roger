from django.shortcuts import render, redirect
from Gestion_Recetas.models import Categoria, Receta
from django.db.models import Q
from django.core.paginator import Paginator #para paginar
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from seguridad.decoradores import groups_required

# Create your views here.
@login_required
@groups_required('Jefe')
def registrar_receta(request):
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        tamanio = request.POST.get('porcion')
        ingredientes = request.POST.get('ingredientes')
        pasos = request.POST.get('preparacion')

        categoria = Categoria.objects.get(idCategoria   =categoria_id)

        nueva_receta = Receta(
            nombreReceta=nombre,
            Categoria=categoria,
            tamanio=tamanio,
            ingredientes=ingredientes,
            pasos=pasos
        )
        nueva_receta.save()
        url = reverse('listar_recetas')
        return redirect(f'{url}?exito=1')
    return render(request, 'registrar_receta.html', {
        'categorias': categorias
    })

@login_required
@groups_required('Jefe')
def listar_recetas(request):
        recetas = Receta.objects.filter(estaHabilitadoReceta=True)
        query = request.GET.get('q', '')
        if query:
            recetas = recetas.filter(
                Q(nombreReceta__icontains=query) | 
                Q(Categoria__nombreCategoria__icontains=query))
            paginaror = Paginator(recetas, 10)

        recetas = recetas.order_by('idReceta')
        paginator = Paginator(recetas, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'listar_recetas.html', {
            'recetas_paginadas': page,
            'query': query
        })

@login_required
@groups_required('Jefe')
def editar_receta(request, idReceta):
    receta = Receta.objects.get(idReceta=idReceta)
    categorias = Categoria.objects.all()
    if request.method == 'POST':
        receta.nombreReceta = request.POST.get('nombre')
        categoria_id = request.POST.get('categoria')
        receta.tamanio = request.POST.get('porcion')
        receta.ingredientes = request.POST.get('ingredientes')
        receta.pasos = request.POST.get('preparacion')

        receta.Categoria = Categoria.objects.get(idCategoria=categoria_id)

        receta.save()
        url = reverse('listar_recetas')
        return redirect(f'{url}?exito=2')
    return render(request, 'editar_receta.html', {
        'receta': receta,
        'categorias': categorias
    })

@login_required
@groups_required('Jefe')
def detalle_receta(request, idReceta):
        receta = Receta.objects.get(idReceta=idReceta)
        categoria = Categoria.objects.get(idCategoria=receta.Categoria.idCategoria)
        return render(request, 'detalle_receta.html', {
            'receta': receta
        })

@login_required
@groups_required('Jefe')
def deshabilitar_receta(request, idReceta):
    receta = Receta.objects.get(idReceta=idReceta)
    receta.estaHabilitadoReceta = False
    receta.save()
    return redirect('listar_recetas')

@login_required
@groups_required('Jefe')
def listar_recetas_deshabilitadas(request):
        recetas = Receta.objects.filter(estaHabilitadoReceta=False)
        query = request.GET.get('q', '')
        if query:
            recetas = recetas.filter(
                Q(nombreReceta__icontains=query) | 
                Q(Categoria__nombreCategoria__icontains=query))
            paginaror = Paginator(recetas, 10)

        recetas = recetas.order_by('idReceta')
        paginator = Paginator(recetas, 10)
        page_number = request.GET.get('page')
        page = paginator.get_page(page_number)
        return render(request, 'listar_recetas_deshabilitadas.html', {
            'recetas_paginadas': page,
            'query': query
        })

@login_required
@groups_required('Jefe')
def habilitar_receta(request, idReceta):
    receta = Receta.objects.get(idReceta=idReceta)
    receta.estaHabilitadoReceta = True
    receta.save()
    return redirect('listar_recetas_deshabilitadas')
from django.shortcuts import render, redirect
from Gestion_Recetas.models import Categoria, Receta
from django.db.models import Q
from django.core.paginator import Paginator #para paginar
from django.urls import reverse

# Create your views here.
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
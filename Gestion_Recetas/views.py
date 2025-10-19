from django.shortcuts import render, redirect
from Gestion_Recetas.models import Categoria, Receta

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
        return redirect('listar_recetas')
    return render(request, 'registrar_receta.html', {
        'categorias': categorias
    })
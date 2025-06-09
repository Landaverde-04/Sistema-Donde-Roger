from django.shortcuts import render
import datetime
from . import models

def ver_inventario(request):
    ultimo_inventario = models.Inventario.objects.all().last()
    if ultimo_inventario is None:
        redirect('crear_inventario')
    return render(request, 'ver_inventario.html')
    
    
def crear_inventario(request):
    if request.method == 'POST':
        current_date = datetime.datetime.now()
        fechaInventario = current_date.strftime('%d/%m/%Y')
        horaInventario = current_date.strftime('%H:%M:%S')

    return render(request, 'crear_inventario.html', {'fecha_inventario': fechaInventario, 'hora_inventario': horaInventario})



    
# Create your views here.

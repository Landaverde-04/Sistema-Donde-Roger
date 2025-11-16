
from django.contrib import admin
from .models import Mesa, ReservaMesa


@admin.register(Mesa)
class MesaAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacidad', 'ubicacion', 'forma', 'estado', 'fila', 'columna')
    list_editable = ('capacidad', 'forma', 'estado', 'fila', 'columna')
    search_fields = ('numero', 'ubicacion')


@admin.register(ReservaMesa)
class ReservaMesaAdmin(admin.ModelAdmin):
    list_display = ('nombre_contacto', 'mesa', 'fecha_hora', 'cantidad_personas', 'estado')
    list_filter = ('estado', 'tipo_reserva')
    search_fields = ('nombre_contacto', 'telefono_contacto')

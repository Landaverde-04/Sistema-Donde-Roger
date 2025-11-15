# reservas_mesa/models.py
from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta





TIPO_RESERVA_CHOICES = [
    ('COMUN', 'Común'),
    ('EVENTO', 'Evento'),
]

ESTADO_RESERVA_CHOICES = [
    ('PENDIENTE', 'Pendiente'),
    ('CONFIRMADA', 'Confirmada'),
    ('CANCELADA', 'Cancelada'),
    ('FINALIZADA', 'Finalizada'),
]

FORMA_MESA_CHOICES = [
    ('CIRCULO', 'Círculo'),
    ('RECT', 'Rectángulo'),
    ('ROMBO', 'Rombo'),
]

ESTADO_MESA_CHOICES = [
    ('LIBRE', 'Libre'),
    ('RESERVADA', 'Reservada'),
    ('OCUPADA', 'Ocupada'),
]


class Mesa(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    capacidad = models.PositiveIntegerField()
    ubicacion = models.CharField(max_length=100, blank=True)

    forma = models.CharField(
        max_length=10,
        choices=FORMA_MESA_CHOICES,
        default='RECT'
    )
    estado = models.CharField(
        max_length=10,
        choices=ESTADO_MESA_CHOICES,
        default='LIBRE'
    )

    # posición dentro del “mapa” (en píxeles, simple)
    pos_x = models.IntegerField(default=50)
    pos_y = models.IntegerField(default=50)


    def get_estado_actual(self):
        """
        Calcula el estado de la mesa según las reservaciones de HOY.
        Regla:
        - 45 minutos a partir de la hora de la reserva:
            - Si estamos dentro de esos 45 min → OCUPADA.
            - Si la hora es futura (hoy) → RESERVADA.
            - Si ya pasaron los 45 min o no hay reservas → LIBRE.
        """
        ahora = timezone.now()
        inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia = inicio_dia + timedelta(days=1)

        reservas_hoy = self.reservas.filter(
            fecha_hora__gte=inicio_dia,
            fecha_hora__lt=fin_dia,
            estado__in=['PENDIENTE', 'CONFIRMADA']
        ).order_by('fecha_hora')

        duracion = timedelta(minutes=45)

        estado = 'LIBRE'
        for r in reservas_hoy:
            # En curso: ocupada
            if r.fecha_hora <= ahora < r.fecha_hora + duracion:
                return 'OCUPADA'
            # Futura: reservada (si aún no encontramos ocupada)
            if r.fecha_hora > ahora:
                estado = 'RESERVADA'

        return estado
   
    def get_reserva_actual(self):
        ahora = timezone.now()
        inicio_dia = ahora.replace(hour=0, minute=0, second=0, microsecond=0)
        fin_dia = inicio_dia + timedelta(days=1)

        reservas_hoy = self.reservas.filter(
            fecha_hora__gte=inicio_dia,
            fecha_hora__lt=fin_dia,
            estado__in=['PENDIENTE', 'CONFIRMADA']
        ).order_by('fecha_hora')

        if not reservas_hoy:
            return None

        duracion = timedelta(hours=2)  # duración aproximada de la reserva

        # 1) Si hay una reserva en curso, devolvemos esa
        for r in reservas_hoy:
            if r.fecha_hora <= ahora < r.fecha_hora + duracion:
                return r

        # 2) Si no hay en curso, devolvemos la próxima futura
        return reservas_hoy[0]
    
    def __str__(self):
        return f"Mesa {self.numero} (capacidad {self.capacidad})"

class ReservaMesa(models.Model):
    # Datos de contacto – SIN relación con ningún cliente registrado
    nombre_contacto = models.CharField(max_length=120)
    telefono_contacto = models.CharField(max_length=20, blank=True)

    mesa = models.ForeignKey(Mesa, on_delete=models.PROTECT, related_name='reservas')
    fecha_hora = models.DateTimeField()
    cantidad_personas = models.PositiveIntegerField()

    tipo_reserva = models.CharField(
        max_length=10,
        choices=TIPO_RESERVA_CHOICES,
        default='COMUN'
    )

    estado = models.CharField(
        max_length=10,
        choices=ESTADO_RESERVA_CHOICES,
        default='PENDIENTE'
    )

    observaciones = models.TextField(blank=True)

    creado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reservas_mesa_creadas'
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['fecha_hora']

    def __str__(self):
        return f"{self.nombre_contacto} - Mesa {self.mesa.numero} - {self.fecha_hora:%d/%m %H:%M}"

    # Para la regla de las 5 horas (HU-32)
    def requiere_confirmacion_urgente(self):
        return self.fecha_hora <= timezone.now() + timedelta(hours=5)

    def es_pasada(self):
        return self.fecha_hora < timezone.now()

    def actualizar_estado_por_tiempo(self, minutos=45):
        """
        Si ya pasaron 'minutos' desde la hora de la reserva y sigue en
        PENDIENTE/CONFIRMADA, la marcamos como FINALIZADA.
        """
        if self.estado in ['PENDIENTE', 'CONFIRMADA']:
            if self.fecha_hora + timedelta(minutes=minutos) < timezone.now():
                self.estado = 'FINALIZADA'
                self.save(update_fields=['estado'])
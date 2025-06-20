from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

class Empleado(models.Model):
    idEmpleado = models.AutoField(primary_key=True)  # Clave primaria autoincremental
    nombresEmpleado = models.CharField(max_length=30)
    apellidosEmpleado = models.CharField(max_length=30)
    duiEmpleado = models.CharField(max_length=10)
    fechaNacimientoEmpleado = models.DateField()
    telEmpleado = models.CharField(max_length=8)
    telEmergenciaEmpleado = models.CharField(max_length=8)
    salarioEmpleado = models.DecimalField(max_digits=10, decimal_places=2)
    experienciaLaboralEmpleado = models.TextField()
    fechaContratacionEmpleado = models.DateField()
    direccionEmpleado = models.CharField(max_length=100, null=True, blank=True)
    contratoEmpleado = models.FileField(upload_to='contratos/', null=True, blank=True)
    estaHabilitadoEmpleado = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombresEmpleado} {self.apellidosEmpleado}"


#Modelo de asistencia
User = get_user_model()

class Asistencia(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateField(default=timezone.now)
    horaEntrada = models.TimeField(null=True, blank=True)
    horaSalida = models.TimeField(null=True, blank=True)

    class Meta:
        db_table = 'Asistencia'

    def __str__(self):
        nombre = self.usuario.idEmpleado.nombre if self.usuario.idEmpleado else self.usuario.username
        return f"{nombre} - {self.fecha}"
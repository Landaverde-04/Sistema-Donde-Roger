from django.db import models

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

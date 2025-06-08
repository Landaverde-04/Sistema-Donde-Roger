from django.db import models

#from usersapp.models import Usuario --> quitar cuando Usuario exista (no fue generado por IA att: Jorge)

class Empleado(models.Model):
    idEmpleado = models.AutoField(primary_key=True, db_column='idEmpleado')
   # idUsuario = models.ForeignKey('usersapp.Usuario', on_delete=models.SET_NULL, null=True)
    nombresEmpleado = models.CharField(max_length=30)
    apellidosEmpleado = models.CharField(max_length=30)
    duiEmpleado = models.CharField(max_length=10)
    fechaNacimientoEmpleado = models.DateField()
    telEmpleado = models.CharField(max_length=8)
    telEmergenciaEmpleado = models.CharField(max_length=8)
    salarioEmpleado = models.DecimalField(max_digits=6, decimal_places=2)
    experienciaLaboral = models.TextField()
    fechaContratacion = models.DateField()
    contratoEmpleado = models.TextField()

    def __str__(self):
        return f"{self.nombresEmpleado} {self.apellidosEmpleado}"

from django.db import models

class Proveedor(models.Model):

    idProveedor = models.AutoField(primary_key=True)
    nombreEncargado = models.CharField(max_length=30)
    apellidoEncargado = models.CharField(max_length=30)
    nombreEmpresa = models.CharField(max_length=50)
    tieneIva = models.BooleanField(default=False)
    telProveedor = models.CharField(max_length=9)
    duiEncargado = models.CharField(max_length=10)
    emailProveedor = models.EmailField(max_length=50)
    ubicacionProveedor = models.TextField()
    logoURL = models.TextField()
    estaHabilitadoProveedor = models.BooleanField(default=True)

    class Meta:
        db_table = 'Proveedor'

    def __str__(self):
        return self.nombreEncargado+ " - "+ self.nombreEmpresa
    

class HorarioProveedor(models.Model):

        idProveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
        idHorario = models.AutoField(primary_key=True)
        horaApertura = models.TimeField()
        horaCierre = models.TimeField()
        diaSemana = models.CharField(max_length=15)

        class Meta:
            db_table = 'HorarioProveedor'
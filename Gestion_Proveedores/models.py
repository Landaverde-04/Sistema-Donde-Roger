from django.db import models

class Proveedor(models.Model):

    idProveedor = models.AutoField(primary_key=True)
    nombreEncargado = models.CharField(max_length=30)
    apellidoEncargado = models.CharField(max_length=30)
    nombreEmpresa = models.CharField(max_length=50)
    tieneIva = models.BooleanField(default=False)
    telProveedor = models.CharField(max_length=8)
    duiEncargado = models.CharField(max_length=10)
    emailProveedor = models.EmailField(max_length=50)
    ubicacionProveedor = models.TextField()
    logoURL = models.TextField()
    
    def __str__(self):
        return self.nombreEncargado+ " - "+ self.nombreEmpresa
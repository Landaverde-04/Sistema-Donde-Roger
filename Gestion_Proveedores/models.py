from django.db import models

class Proveedor(models.Model):

    idProveedor = models.CharField(max_length=4, primary_key=True) #iria?
    nombreEncargado = models.CharField(max_length=30)
    apellidoEncargado = models.CharField(max_length=30)
    nombreEmpresa = models.CharField(max_length=50)
    tieneIva = models.BooleanField(default=False)
    telProveedor = models.CharField(max_length=8)
    duiEncargado = models.CharField(max_length=10)
    emailProveedor = models.EmailField(max_length=50)#queda como emailfield debido a la validacion de xys@abc.com
    ubicacionProveedor = models.TextField()
    logoURL = models.TextField()
    horarioApertura = models.TimeField() #timefield o charfield o textfield?
    horarioCierre = models.TimeField()

    def __str__(self):
        return self.nombreEncargado+ " - "+ self.nombreEmpresa
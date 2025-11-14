from django.db import models

# Create your models here.
class Cliente(models.Model):
    idCliente = models.AutoField(primary_key=True)
    nombreCliente = models.CharField(max_length=30)
    apellidoCliente = models.CharField(max_length=30)
    duiCliente = models.CharField(max_length=10)
    telefonoCliente = models.CharField(max_length=9)
    emailCliente = models.EmailField(max_length=50)
    nacimientoCliente = models.DateField()
    estaHabilitadoCliente = models.BooleanField(default=True)

    class Meta:
        db_table = 'Cliente'

    def __str__(self):
        return self.nombreCliente

class DireccionCliente(models.Model):
    idCliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    idDireccion = models.AutoField(primary_key=True)
    direccion = models.TextField()

    class Meta:
        db_table = 'DireccionCliente'
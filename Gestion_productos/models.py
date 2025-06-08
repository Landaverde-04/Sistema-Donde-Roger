from django.db import models

# Create your models here.
from django.db import models

class Producto(models.Model):
    idProducto = models.CharField(primary_key=True, max_length=5)
    nombreProducto = models.CharField(max_length=50)
    unidadMedida = models.CharField(max_length=20)
    marcaProducto = models.CharField(max_length=20)
    descripcionProducto = models.TextField()

    def __str__(self):
        return self.nombreProducto

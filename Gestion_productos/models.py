from django.db import models

# Create your models here.
from django.db import models

class Producto(models.Model):
    idProducto = models.AutoField(primary_key=True)
    nombreProducto = models.CharField(max_length=50)
    unidadMedida = models.CharField(max_length=20)
    marcaProducto = models.CharField(max_length=20)
    descripcionProducto = models.TextField()

    class Meta:
        db_table = 'Producto'
        
    def __str__(self):
        return self.nombreProducto

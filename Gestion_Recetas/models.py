from django.db import models
from Gestion_Menu.models import CategoriaProductoMenu

# Create your models here.
class Receta(models.Model):
    idReceta = models.AutoField(primary_key=True)
    nombreReceta = models.CharField(max_length=50)
    Categoria = models.ForeignKey(CategoriaProductoMenu, on_delete=models.CASCADE)
    tamanio = models.CharField(max_length=20)
    ingredientes = models.TextField()
    pasos = models.TextField()
    estaHabilitadoReceta = models.BooleanField(default=True)

    class Meta:
        db_table = 'Receta'
    def __str__(self):
        return self.nombreReceta

from django.db import models

# Create your models here.
class Categoria(models.Model):
    idCategoria = models.AutoField(primary_key=True)
    nombreCategoria = models.CharField(max_length=30)

    class Meta:
        db_table = 'Categoria'
    def __str__(self):
        return self.nombreCategoria


class Receta(models.Model):
    idReceta = models.AutoField(primary_key=True)
    nombreReceta = models.CharField(max_length=50)
    Categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tamanio = models.CharField(max_length=20)
    ingredientes = models.TextField()
    pasos = models.TextField()
    estaHabilitadoReceta = models.BooleanField(default=True)

    class Meta:
        db_table = 'Receta'
    def __str__(self):
        return self.nombreReceta

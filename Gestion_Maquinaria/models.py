from django.db import models

class Maquinaria(models.Model):
    idMaquinaria = models.AutoField(primary_key=True)
    nombreMaquinaria = models.CharField(max_length=120)
    fechaCompraMaquinaria = models.DateField()
    marcaMaquinaria = models.CharField(max_length=80)
    estaHabilitadaMaquinaria = models.BooleanField(default=True)  # soft-delete

    class Meta:
        db_table = "Maquinaria"
        ordering = ["idMaquinaria"]

    def __str__(self):
        return f"{self.nombreMaquinaria} ({self.marcaMaquinaria})"

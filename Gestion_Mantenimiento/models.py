from django.db import models
from django.core.validators import FileExtensionValidator
from Gestion_Maquinaria.models import Maquinaria

class Mantenimiento(models.Model):
    idMantenimiento = models.AutoField(primary_key=True)
    maquinaria = models.ForeignKey(
        Maquinaria,
        on_delete=models.PROTECT,
        related_name='mantenimientos'
    )
    fechaMantenimiento = models.DateField()
    esCorrectivo = models.BooleanField(default=False)
    nombreTecnico = models.CharField(max_length=120)
    fotoAntesURL = models.ImageField(
        upload_to='mantenimientos/antes/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    fotoDespuesURL = models.ImageField(
        upload_to='mantenimientos/despues/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    fotoFacturaURL = models.ImageField(
        upload_to='mantenimientos/facturas/',
        blank=True, null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'Gestion_Mantenimiento_mantenimiento'  # usa la tabla que ya tienes
        ordering = ['-fechaMantenimiento', '-idMantenimiento']

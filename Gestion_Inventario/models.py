from django.db import models
from Gestion_productos import models as models_productos

class Inventario(models.Model):
    idIventario = models.AutoField(primary_key=True)
    # idUsuario = models.ForeignKey('Usuario', on_delete=models.CASCADE, db_column='idUsuario')
    idUsuario = models.CharField(max_length=4)
    fechaInventario = models.DateField()
    horaInventario = models.TimeField(auto_now_add=True)
    estadoInventario = models.BooleanField()
    
    class Meta:
        db_table = 'Inventario'
    
class DetalleInventario(models.Model):
    idDetalleInventario = models.AutoField(primary_key=True)
    idInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE,db_column='idInventario', to_field='idIventario')
    idProducto = models.ForeignKey(models_productos.Producto, on_delete=models.CASCADE,db_column='idProducto')
    fechaIngreso = models.DateField()
    horaIngreso = models.TimeField()
    fechaCaducidad = models.DateField()
    cantidadProducto = models.DecimalField(max_digits=4, decimal_places=2)
    
    class Meta:
        db_table = 'DetalleInventario'

# Create your models here.

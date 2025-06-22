from django.db import models
from Gestion_productos import models as models_productos    #Importar los modelos de los productos
from seguridad import models as models_seguridad    #importar los modelos de seguridad

class Inventario(models.Model): #Tabla de la bd para los inventarios
    idInventario = models.AutoField(primary_key=True)
    idUsuario = models.ForeignKey(models_seguridad.Usuario, on_delete=models.CASCADE, db_column='idUsuario', null=False)
    fechaInventario = models.DateField()
    horaInventario = models.TimeField(auto_now_add=True)
    sePuedeEditar = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'Inventario'
    
class DetalleInventario(models.Model):
    idDetalleInventario = models.AutoField(primary_key=True)
    idInventario = models.ForeignKey(Inventario, on_delete=models.CASCADE,db_column='idInventario', to_field='idInventario')
    idProducto = models.ForeignKey(models_productos.Producto, on_delete=models.CASCADE,db_column='idProducto')
    fechaIngreso = models.DateField()
    horaIngreso = models.TimeField()
    fechaCaducidad = models.DateField()
    cantidadProducto = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        db_table = 'DetalleInventario'

# Create your models here.

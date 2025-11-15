from django.db import models
from Gestion_Clientes import models as models_clientes
from Gestion_Menu import models as models_menu
from empleado.models import Empleado

class EstadoPedidoCliente(models.Model):
    idEstado = models.AutoField(primary_key=True)
    nombreEstado = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'EstadoPedidoCliente'
        
    def __str__(self):
        return self.nombreEstado
class TipoPedidoCliente(models.Model):
    idTipoPedido = models.AutoField(primary_key=True)
    nombreTipoPedido = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'TipoPedido'
    
    def __str__(self):
        return self.nombreTipoPedido
class PedidoCliente(models.Model):
    idPedidoCliente = models.AutoField(primary_key=True)
    idCliente = models.ForeignKey(models_clientes.Cliente, on_delete=models.CASCADE, null=True)
    tipoPedido = models.ForeignKey(TipoPedidoCliente, on_delete=models.CASCADE)
    mesasPedido = models.CharField(max_length=100, null=True)
    direccionPedido = models.CharField(max_length=100, null=True)
    horaRecoger = models.DateTimeField(null=True)
    fechaPedidoCliente = models.DateField()
    horaPedidoCliente = models.DateTimeField()
    numCorrelativo = models.CharField(max_length=20)
    totalPedido = models.DecimalField(max_digits=10, decimal_places=2)
    comentario = models.TextField(null=True)
    estadoPedido = models.ForeignKey(EstadoPedidoCliente, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Pedido'
    
    def __str__(self):
        return self.numCorrelativo
    
class DetallePedido(models.Model):
    idDetallePedido = models.AutoField(primary_key=True)
    idPedidoCliente = models.ForeignKey(PedidoCliente, on_delete=models.CASCADE)
    idProducto = models.ForeignKey(models_menu.ProductoMenu, on_delete=models.CASCADE)
    cantidadPedido = models.IntegerField()
    subtotalPedido = models.DecimalField(max_digits=20, decimal_places=2)
    
    class Meta:
        db_table = 'DetallePedido'
    
    def __str__(self):
        return self.idDetallePedido

    
    
class ManipulacionPedido(models.Model):
    idManipulacion = models.AutoField(primary_key=True)
    esNuevoRegistro = models.BooleanField(default=False)
    horaManipulacion = models.DateTimeField()
    fechaManipulacion = models.DateField()
    idEmpleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    IdPedidoCliente = models.ForeignKey(PedidoCliente, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'ManipulacionPedido'
        
    def __str__(self):
        return str(self.idManipulacion)
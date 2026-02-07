from django.db import models
from Gestion_Proveedores.models import Proveedor, ProductoProveedor

class PedidoProveedor(models.Model):
    idPedidoProveedor = models.AutoField(primary_key=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, related_name="pedidos")
    fechaPedidoProveedor = models.DateTimeField(auto_now_add=True)
    sePuedeEditarPP = models.BooleanField(default=True)
    totalPP = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    finalizado = models.BooleanField(default=False)
    pdf_pedido = models.FileField(upload_to='pedidos_proveedores/', null=True, blank=True)

    class Meta:
        db_table = 'PedidoProveedor'

    def __str__(self):
        return f"Pedido #{self.idPedidoProveedor} - {self.proveedor.nombreEmpresa}"

    def calcular_total(self):
        total = sum(detalle.subTotalPP for detalle in self.detalles.all())
        self.totalPP = total
        self.save()


class DetallePedidoProveedor(models.Model):
    idDetallePedidoProveedor = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(PedidoProveedor, on_delete=models.CASCADE, related_name='detalles')
    producto = models.ForeignKey(ProductoProveedor, on_delete=models.CASCADE)
    cantidadPP = models.DecimalField(max_digits=8, decimal_places=2)
    subTotalPP = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    class Meta:
        db_table = 'DetallePedidoProveedor'
        unique_together = ('pedido', 'producto')

    def __str__(self):
        return f"{self.producto.nombreProductoProveedor} x {self.cantidadPP}"

    def save(self, *args, **kwargs):
        self.subTotalPP = self.cantidadPP * self.producto.precioProductoProveedor
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

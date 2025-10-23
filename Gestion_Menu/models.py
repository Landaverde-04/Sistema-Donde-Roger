from django.db import models

#Seccion de MENU PARA CLIENTES

class CategoriaProductoMenu(models.Model):
    idCategoriaProductoMenu = models.AutoField(primary_key=True)
    nombreCategoriaProductoMenu = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'CategoriaProductoMenu'
        
    def __str__(self):
        return self.nombreCategoriaProductoMenu
    

class ProductoMenu(models.Model):
    idProductoMenu = models.AutoField(primary_key=True)
    idCategoriaProductoMenu = models.ForeignKey(CategoriaProductoMenu, on_delete=models.CASCADE)
    nombreProductoMenu = models.CharField(max_length=50)
    tamanioProductoMenu = models.CharField(max_length=20)
    descripcionProductoMenu = models.TextField()
    estaHabilitadoProductoMenu = models.BooleanField(default=True)
    precioProductoMenu = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        db_table = 'ProductoMenu'
    
    def __str__(self):
        return self.nombreProductoMenu
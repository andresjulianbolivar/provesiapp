from django.db import models
from bodegas.models import Bodega
from productos.models import Producto

class Inventario(models.Model):
    producto = models.ForeignKey(Producto, on_delete='CASCADE')
    bodega = models.ForeignKey(Bodega, on_delete='CASCADE')
    cantidad = models.PositiveIntegerField()
    
    def __str__(self):
        return '{} {} {}'.format(self.producto,self.bodega,self.cantidad)
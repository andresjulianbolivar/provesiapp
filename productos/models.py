from django.db import models
from bodegas.models import Bodega

class Producto(models.Model):
    codigo = models.PositiveIntegerField(primary_key=True)
    nombre = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    talla = models.CharField(max_length=50)
    descripcion = models.TextField()
    bodegas = models.ManyToManyField(Bodega, through='inventarios.Inventario')
    
    def __str__(self):
        return '{} {} {} {} {}'.format(self.codigo,self.nombre,self.color,self.talla,self.descripcion)
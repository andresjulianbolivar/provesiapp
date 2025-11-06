from django.db import models
from facturaciones.models import Pedido

class Cotizacion(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, default=None)
    transportadora = models.CharField(max_length=50)
    precio = models.FloatField(null=True, blank=True, default=None)
    tiempo = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return '%s %s' % (self.pedido, self.transportadora,self.precio,self.tiempo)
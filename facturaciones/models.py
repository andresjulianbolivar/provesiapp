from django.db import models

class Factura(models.Model):
    rubro_total = models.FloatField()
    orden_produccion = models.BooleanField()
    pedido=models.OneToOneField('Pedido', on_delete=models.CASCADE, null=True, blank=True, related_name="factura")

    def __str__(self):
        return f"Factura #{self.id} - Total: {self.rubro_total}"


class Pedido(models.Model):
    fecha = models.DateField()
    vip = models.BooleanField()
    #factura = models.OneToOneField(Factura, on_delete=models.CASCADE, related_name="pedido")

    def __str__(self):
        return f"Pedido #{self.id} - {self.fecha}"


class Cantidad(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="cantidades")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name="cantidades")
    unidades = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.unidades}x {self.producto}"

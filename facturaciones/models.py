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
    estado = models.CharField(max_length=50, default="Verificado")
    def __str__(self):
        return f"Pedido #{self.id} - {self.fecha} - VIP: {self.vip} - Estado: {self.estado}"


class Cantidad(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="cantidades")
    producto = models.ForeignKey('productos.Producto', on_delete=models.CASCADE, related_name="cantidades")
    unidades = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.unidades}x {self.producto}"
    


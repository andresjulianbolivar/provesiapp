from django.db import models

class Bodega(models.Model):
    ciudad = models.CharField(max_length=50)
    direccion = models.TextField()
    
    def __str__(self):
        return '{} {}'.format(self.ciudad, self.direccion)
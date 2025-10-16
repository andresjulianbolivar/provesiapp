from django.core.management.base import BaseCommand
from productos.models import Producto
from bodegas.models import Bodega
from inventarios.models import Inventario

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba para la ASR de consulta de stock por código de producto.'

    def handle(self, *args, **options):
        # Crear bodegas usando los campos existentes (ciudad y direccion)
        bodega1, _ = Bodega.objects.get_or_create(ciudad="Bogotá", direccion="Calle 1 # 23-45")
        bodega2, _ = Bodega.objects.get_or_create(ciudad="Medellín", direccion="Carrera 7 # 89-10")

        # Crear productos
        producto1, _ = Producto.objects.get_or_create(codigo=1001, defaults={
            "nombre": "Camiseta",
            "color": "Rojo",
            "talla": "M",
            "descripcion": "Camiseta deportiva",
            "precio": 29.99
        })
        producto2, _ = Producto.objects.get_or_create(codigo=1002, defaults={
            "nombre": "Pantalón",
            "color": "Azul",
            "talla": "L",
            "descripcion": "Pantalón de mezclilla",
            "precio": 49.99
        })
        producto3, _ = Producto.objects.get_or_create(codigo=1003, defaults={
            "nombre": "Falda",
            "color": "Agua marina",
            "talla": "L",
            "descripcion": "Falda de verano",
            "precio": 39.99
        })
        # Crear inventarios
        Inventario.objects.get_or_create(producto=producto1, bodega=bodega1, defaults={"cantidad": 50})
        Inventario.objects.get_or_create(producto=producto1, bodega=bodega2, defaults={"cantidad": 20})
        Inventario.objects.get_or_create(producto=producto2, bodega=bodega1, defaults={"cantidad": 15})
        Inventario.objects.get_or_create(producto=producto2, bodega=bodega2, defaults={"cantidad": 30})
        Inventario.objects.get_or_create(producto=producto3, bodega=bodega1, defaults={"cantidad": 25})
        Inventario.objects.get_or_create(producto=producto3, bodega=bodega2, defaults={"cantidad": 10})

        self.stdout.write(self.style.SUCCESS('Datos de prueba para la ASR poblados correctamente.'))

from django.core.management.base import BaseCommand
from productos.models import Producto
from bodegas.models import Bodega
from inventarios.models import Inventario
# correr la base de datos con:
#python manage.py poblar_asr

class Command(BaseCommand):
    help = 'Pobla la base de datos con datos de prueba para la ASR de consulta de stock por código de producto.'

    def handle(self, *args, **options):
        # Crear bodegas
        bodega1, _ = Bodega.objects.get_or_create(nombre="Bodega Central", defaults={"direccion": "Calle 1 # 23-45"})
        bodega2, _ = Bodega.objects.get_or_create(nombre="Bodega Norte", defaults={"direccion": "Carrera 7 # 89-10"})

        # Crear productos
        producto1, _ = Producto.objects.get_or_create(codigo=1001, defaults={
            "nombre": "Camiseta",
            "color": "Rojo",
            "talla": "M",
            "descripcion": "Camiseta deportiva"
        })
        producto2, _ = Producto.objects.get_or_create(codigo=1002, defaults={
            "nombre": "Pantalón",
            "color": "Azul",
            "talla": "L",
            "descripcion": "Pantalón de mezclilla"
        })

        # Crear inventarios
        Inventario.objects.get_or_create(producto=producto1, bodega=bodega1, defaults={"cantidad": 50})
        Inventario.objects.get_or_create(producto=producto1, bodega=bodega2, defaults={"cantidad": 20})
        Inventario.objects.get_or_create(producto=producto2, bodega=bodega1, defaults={"cantidad": 15})
        Inventario.objects.get_or_create(producto=producto2, bodega=bodega2, defaults={"cantidad": 30})

        self.stdout.write(self.style.SUCCESS('Datos de prueba para la ASR poblados correctamente.'))

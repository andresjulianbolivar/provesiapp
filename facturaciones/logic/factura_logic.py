import datetime
from productos.models import Producto
from ..models import Factura, Pedido
from . import pedido_logic as pedido_logic

def get_factura(id):
    queryset = Factura.objects.filter(id=id)
    return queryset

def get_facturas():
    queryset = Factura.objects.all()
    return queryset

def create_factura(pedido: Pedido):
    rubro_total = 0.0
    orden_produccion = False

    for cantidad in pedido.cantidades.all():
        producto_obj = Producto.objects.get(codigo=cantidad.producto.codigo)
        unidades = cantidad.unidades
        rubro_total += producto_obj.precio * unidades

    factura = Factura.objects.create(rubro_total=rubro_total, orden_produccion=orden_produccion, pedido=pedido)

    return factura

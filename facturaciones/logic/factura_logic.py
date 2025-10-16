import datetime
from productos.models import Producto
from ..models import Factura, Pedido
import pedido_logic as pedido_logic

def get_factura(id):
    queryset = Factura.objects.filter(id=id)
    return queryset

def get_facturas():
    queryset = Factura.objects.all()
    return queryset

def create_factura(productos_cantidades, vip=False):
    rubro_total = 0.0
    orden_produccion = False
    pedido=pedido_logic.create_pedido(productos_cantidades, vip)

    for producto in productos_cantidades:
        producto_obj = Producto.objects.get(codigo=producto['codigo'])
        unidades= producto["unidades"]
        rubro_total+= producto_obj.precio * unidades

    factura= Factura.objects.create(total=rubro_total, orden_produccion=orden_produccion, pedido=pedido)

    return factura
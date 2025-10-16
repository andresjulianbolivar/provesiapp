from datetime import datetime
from ..models import Pedido, Cantidad


def create_pedido(productos_cantidades, vip):
    pedido = Pedido.objects.create(
        fecha=datetime.date.today(),
        vip=vip
    )
    
    for item in productos_cantidades:
        new_cantidad=Cantidad.objects.create(
            pedido=pedido,
            producto_id=item['codigo'],
            unidades=item['unidades']
        )
        new_cantidad.save()
    return pedido
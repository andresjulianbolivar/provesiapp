import requests
from django.conf import settings



from datetime import datetime
from ..models import Pedido, Cantidad



def create_pedido(productos_cantidades, vip, estado="Verificado"):
    pedido = Pedido.objects.create(
        fecha=datetime.today().strftime('%Y-%m-%d'),
        vip=vip,
        estado=estado
    )
    
    for item in productos_cantidades:
        new_cantidad=Cantidad.objects.create(
            pedido=pedido,
            producto_id=item['codigo'],
            unidades=item['unidades']
        )
        new_cantidad.save()

    return pedido

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


def crear_pedido_en_ms(productos_cantidades, vip: bool):
    """
    Llama al microservicio de pedidos para crear el pedido.
    """
    base = settings.PEDIDOS_MS_BASE_URL.rstrip("/")
    url = f"{base}/ManejadorPedidos/crear-pedido/"

    payload = {
        "productos_cantidades": productos_cantidades,
        "vip": vip,
    }

    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()
import requests
from django.conf import settings


def ms_crear_pedido(productos_cantidades, vip: bool):
    """
    Llama al microservicio de pedidos para crear un pedido.
    No cambia la lógica legacy, solo la complementa.
    """
    base = settings.PEDIDOS_MS_BASE_URL.rstrip("/")
    url = f"{base}/ManejadorPedidos/crear-pedido/"

    payload = {
        "productos_cantidades": productos_cantidades,
        "vip": vip,
    }

    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()  # ej: {"pedido_id": ..., "estado": ..., "vip": ...}


def ms_crear_factura(pedido_id: int):
    """
    Llama al microservicio de pedidos para crear una factura
    a partir de un pedido existente.
    """
    base = settings.PEDIDOS_MS_BASE_URL.rstrip("/")
    url = f"{base}/ManejadorPedidos/crear-factura/"

    payload = {"pedido_id": pedido_id}

    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()  # ej: {"factura_id": ..., "total": "...", "pedido_id": ...}

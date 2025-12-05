# facturaciones/logic/ms_client.py
import requests
from django.conf import settings


def _base_url() -> str:
    return settings.PEDIDOS_MS_BASE_URL.rstrip("/")


def ms_crear_pedido(productos_cantidades, vip: bool):
    """
    Llama al microservicio de pedidos para crear un pedido.
    """
    url = f"{_base_url()}/ManejadorPedidos/crear-pedido/"

    payload = {
        "productos_cantidades": productos_cantidades,
        "vip": vip,
    }

    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()  # {"pedido_id": ..., "estado": ..., "vip": ...}


def ms_crear_factura(pedido_id: int):
    """
    Llama al microservicio de pedidos para crear una factura
    a partir de un pedido existente.
    """
    url = f"{_base_url()}/ManejadorPedidos/crear-factura/"

    payload = {"pedido_id": pedido_id}

    resp = requests.post(url, json=payload, timeout=5)
    resp.raise_for_status()
    return resp.json()  # {"factura_id": ..., "total": "...", "pedido_id": ...}


def ms_listar_facturas_pendientes():
    """
    Devuelve lista de facturas del MS.
    """
    url = f"{_base_url()}/ManejadorPedidos/facturas-pendientes/"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()  # lista de dicts: {"id", "rubro_total", "pedido_id", ...}


def ms_listar_pedidos_verificados():
    """
    Devuelve lista de pedidos en estado 'Verificado' desde el MS.
    """
    url = f"{_base_url()}/ManejadorPedidos/pedidos-verificados/"
    resp = requests.get(url, timeout=5)
    resp.raise_for_status()
    return resp.json()  # lista de dicts: {"id", "fecha", "vip", "estado"}

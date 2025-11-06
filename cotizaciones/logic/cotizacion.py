from ..models import Cotizacion
import requests

def crear_cotizacion(pedido_s):
    url = 'http://127.0.0.1:8000/cotizar/'
    payload = {"peso":5}
    try:
        response = requests.post(url, json=payload, timeout=5)
        response.raise_for_status()
        data = response.json()
        cotizaciones = []
        for item in data:
            cotizacion = Cotizacion.objects.create(
                pedido = pedido_s,
                transportadora = item.get("transportadora"),
                precio = item.get("precio"),
                tiempo = item.get("tiempo"),
                peso = item.get("peso")
            )
            cotizaciones.append(cotizacion)
        return cotizaciones
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] No se pudo conectar con el API de transportadora: {e}")
        return None
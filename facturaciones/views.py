from django.http import JsonResponse
from django.shortcuts import render

from facturaciones.logic.factura_logic import create_factura

# Create your views here.
def generar_factura(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            productos_cantidades=data.get("productos_cantidades", [])
            vip=data.get("vip", False)
            factura=create_factura(productos_cantidades, vip)
            return JsonResponse({
                "factura_id": factura.id,
                "total": factura.total,
                "pedido_id": factura.pedido.id if factura.pedido else None
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)
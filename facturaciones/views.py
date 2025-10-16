import json
from django.http import JsonResponse
from django.shortcuts import render

from facturaciones.logic.factura_logic import create_factura
from productos.models import Producto

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

def crear_factura(request):
    productos = Producto.objects.all()
    mensaje = ""
    if request.method == "POST":
        productos_cantidades = []
        for producto in productos:
            cantidad = int(request.POST.get(f"cantidad_{producto.codigo}", 0))
            if cantidad > 0:
                productos_cantidades.append({"codigo": producto.codigo, "unidades": cantidad})
        if productos_cantidades:
            create_factura(productos_cantidades)
            mensaje = "¡Factura creada exitosamente!"
        else:
            mensaje = "Debes ingresar al menos una cantidad."
    return render(request, "facturaciones/crear_factura.html", {
        "productos": productos,
        "mensaje": mensaje
    })
    
from django.shortcuts import render
from .models import Factura

def facturas_pendientes(request):
    facturas = Factura.objects.all() 
    return render(request, "facturaciones/facturas_pendientes.html", {"facturas": facturas})
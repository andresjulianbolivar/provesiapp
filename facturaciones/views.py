# facturaciones/views.py
import json

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from productos.models import Producto
from provesiapp.auth0backend import getRole

from .models import Factura, Pedido
from .logic.factura_logic import create_factura as legacy_create_factura
from .logic.pedido_logic import create_pedido as legacy_create_pedido
from .logic.ms_client import (    
    ms_crear_pedido,
    ms_crear_factura,
    ms_listar_facturas_pendientes,
    ms_listar_pedidos_verificados,
)


# --- API legacy (no HTML) - adaptar en el futuro ---

def generar_factura(request):
    """
    API legacy
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            productos_cantidades = data.get("productos_cantidades", [])
            vip = data.get("vip", False)

            # Legacy: Pedido "en memoria" y create_factura local
            factura = legacy_create_factura(Pedido(productos_cantidades, vip))

            return JsonResponse(
                {
                    "factura_id": factura.id,
                    "total": factura.rubro_total,
                    "pedido_id": factura.pedido.id if factura.pedido else None,
                },
                status=201,
            )
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Método no permitido"}, status=405)


# --- Vistas HTML ---


@login_required
def crear_pedido(request):
    """
    Esta vista solo construye el formulario y manda los datos al MS.
    """
    role = getRole(request)
    if role != "Gerencia WMS":
        return HttpResponse("Unauthorized User", status=403)

    productos = Producto.objects.all()
    mensaje = ""

    if request.method == "POST":
        productos_cantidades = []
        for producto in productos:
            cantidad = int(request.POST.get(f"cantidad_{producto.codigo}", 0))
            if cantidad > 0:
                productos_cantidades.append(
                    {
                        "codigo": producto.codigo,
                        "unidades": cantidad,
                        "nombre": producto.nombre,
                        "precio": float(producto.precio),
                    }
                )

        if productos_cantidades:
            vipp = bool(request.POST.get("vip", False))
            try:
                resp = ms_crear_pedido(productos_cantidades, vip=vipp)
                pedido_id_ms = resp.get("pedido_id")
                mensaje = f"¡Pedido creado exitosamente en el MS! ID: {pedido_id_ms}"
            except Exception as e:
                mensaje = f"Error llamando al MS de pedidos: {e}"
        else:
            mensaje = "Debes ingresar al menos una cantidad."

    return render(
        request,
        "facturaciones/crear_pedido.html",
        {
            "productos": productos,
            "mensaje": mensaje,
        },
    )



def facturas_pendientes(request):
    try:
        facturas = ms_listar_facturas_pendientes()
    except Exception as e:
        # En caso de falla del MS, mostramos pantalla con error
        return render(
            request,
            "facturaciones/facturas_pendientes.html",
            {
                "facturas": [],
                "error": f"Error consultando el microservicio de pedidos: {e}",
            },
        )

    return render(
        request,
        "facturaciones/facturas_pendientes.html",
        {
            "facturas": facturas,
        },
    )



def crear_factura(request):
    """
    se hacen vía microservicio de pedidos.
    """
    mensaje = ""

    try:
        pedidos_verificados = ms_listar_pedidos_verificados()
    except Exception as e:
        pedidos_verificados = []
        mensaje = f"Error consultando pedidos verificados en el MS: {e}"

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")

        if not pedido_id:
            mensaje = "Debes seleccionar un pedido válido."
        else:
            try:
                # MS para crear la factura
                resp = ms_crear_factura(int(pedido_id))
                factura_id = resp.get("factura_id")
                total = resp.get("total")

                mensaje = (
                    f"Factura #{factura_id} creada en el MS "
                    f"para el pedido #{pedido_id}. Total: {total}."
                )
            except Exception as e:
                mensaje = f"Ocurrió un error al crear la factura en el MS: {e}"

    return render(
        request,
        "facturaciones/crear_factura.html",
        {
            "mensaje": mensaje,
            "pedidos_verificados": pedidos_verificados,
        },
    )

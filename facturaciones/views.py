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
from .logic.ms_client import ms_crear_pedido, ms_crear_factura


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
    Vista HTML legacy de crear pedido.

    Cambios:
    - Sigue usando Productos + template legacy.
    - PERO llama al MS de pedidos.
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
                        # info extra para el MS de pedidos
                        "nombre": producto.nombre,
                        "precio": float(producto.precio),
                    }
                )

        if productos_cantidades:
            vipp = bool(request.POST.get("vip", False))

            # Lógica legacy
            legacy_create_pedido(productos_cantidades, vip=vipp)

            # Llamada microservicio de pedidos
            try:
                ms_response = ms_crear_pedido(productos_cantidades, vip=vipp)
                pedido_id_ms = ms_response.get("pedido_id")
                mensaje = f"¡Pedido creado exitosamente! (MS ID: {pedido_id_ms})"
            except Exception as e:
                mensaje = f"Pedido local creado, pero falló el MS de pedidos: {e}"
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
    """
    Vista legacy que lista facturas locales.
    """
    facturas = Factura.objects.all()
    return render(
        request,
        "facturaciones/facturas_pendientes.html",
        {"facturas": facturas},
    )


def crear_factura(request):
    """
    Vista HTML legacy para crear factura.

    Cambios:
    - Sigue usando los modelos locales para mostrar pedidos verificados.
    - También intenta crearla en el MS.
    """
    mensaje = ""
    pedidos_verificados = Pedido.objects.filter(estado="Verificado")

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")

        if not pedido_id:
            mensaje = "Debes seleccionar un pedido válido."
        else:
            try:
                pedido = Pedido.objects.get(id=pedido_id)

                # 1) Lógica legacy local
                factura = legacy_create_factura(pedido)

                pedido.estado = "Empacado x despachar"
                pedido.save()

                mensaje = (
                    f"Factura #{factura.id} creada para el pedido #{pedido.id} (local)."
                )

                # Llamada microservicio de pedidos
                try:
                    ms_resp = ms_crear_factura(pedido.id)
                    factura_ms_id = ms_resp.get("factura_id")
                    mensaje += f" También se creó en el MS (ID factura MS: {factura_ms_id})."
                except Exception as e:
                    mensaje += f" Pero falló la creación en el MS de pedidos: {e}"

            except Pedido.DoesNotExist:
                mensaje = "El pedido seleccionado no existe."
            except Exception as e:
                mensaje = f"Ocurrió un error al crear la factura: {e}"

    return render(
        request,
        "facturaciones/crear_factura.html",
        {
            "mensaje": mensaje,
            "pedidos_verificados": pedidos_verificados,
        },
    )

import json
from django.http import JsonResponse
from django.shortcuts import render

from facturaciones.logic.factura_logic import create_factura
from facturaciones.logic.pedido_logic import create_pedido
from productos.models import Producto
from provesiapp.auth0backend import getRole
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.
def generar_factura(request):
    if request.method=="POST":
        try:
            data=json.loads(request.body)
            productos_cantidades=data.get("productos_cantidades", [])
            vip=data.get("vip", False)
            factura=create_factura(Pedido(productos_cantidades, vip))
            return JsonResponse({
                "factura_id": factura.id,
                "total": factura.rubro_total,
                "pedido_id": factura.pedido.id if factura.pedido else None
            }, status=201)
        except Exception as e:
            return JsonResponse({
                "error": str(e)
            }, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

@login_required
def crear_pedido(request):
    role = getRole(request)
    if role == "Gerencia WMS":
        productos = Producto.objects.all()
        mensaje = ""
        if request.method == "POST":
            productos_cantidades = []
            for producto in productos:
                cantidad = int(request.POST.get(f"cantidad_{producto.codigo}", 0))
                if cantidad > 0:
                    productos_cantidades.append({"codigo": producto.codigo, "unidades": cantidad})
            if productos_cantidades:
                vipp=request.POST.get("vip", False)
                create_pedido(productos_cantidades, vip=vipp)
                mensaje = "¡Pedido creado exitosamente!"
            else:
                mensaje = "Debes ingresar al menos una cantidad."
        return render(request, "facturaciones/crear_pedido.html", {
            "productos": productos,
            "mensaje": mensaje
        })
    else:
        return HttpResponse("Unauthorized User")
    
from django.shortcuts import render
from .models import Factura, Pedido

def facturas_pendientes(request):
    facturas = Factura.objects.all() 
    return render(request, "facturaciones/facturas_pendientes.html", {"facturas": facturas})

def crear_factura(request):
    mensaje = ""
    pedidos_verificados = Pedido.objects.filter(estado="Verificado")

    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")

        if not pedido_id:
            mensaje = "Debes seleccionar un pedido válido."
        else:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                # Crear factura (si tu lógica ya lo maneja, simplemente llámala)
                factura = create_factura(pedido)
                
                # Opcional: cambiar estado del pedido
                pedido.estado = "Empacado x despachar"
                pedido.save()

                mensaje = f"Factura #{factura.id} creada para el pedido #{pedido.id}."
            except Pedido.DoesNotExist:
                mensaje = "El pedido seleccionado no existe."
            except Exception as e:
                mensaje = f"Ocurrió un error al crear la factura: {e}"

    return render(request, "facturaciones/crear_factura.html", {
        "mensaje": mensaje,
        "pedidos_verificados": pedidos_verificados
    })
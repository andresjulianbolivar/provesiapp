from django.shortcuts import render
from facturaciones.models import Pedido
from .models import Cotizacion
from cotizaciones.logic.cotizacion import crear_cotizacion

# Create your views here.
def create_cotizacion(request):
    mensaje = ""
    if request.method == "POST":
        pedido_id = request.POST.get("pedido_id")

        if not pedido_id:
            mensaje = "Debes seleccionar un pedido válido."
        else:
            try:
                pedido = Pedido.objects.get(id=pedido_id)
                
                if pedido.estado != "Empacado x despachar":
                    mensaje = f"El pedido {pedido.id} no se puede despachar aun."
                else:
                    crear_cotizacion(pedido)
                    mensaje = f"Cotizaciones para el pedido #{pedido.id} creadas."
            except Pedido.DoesNotExist:
                mensaje = "El pedido seleccionado no existe."
            except Exception as e:
                mensaje = f"Ocurrió un error al crear la factura: {e}"

    return render(request, "cotizaciones/crear_cotizacion.html", {
        "mensaje": mensaje
    })
    
def cotizaciones(request):
    id = request.GET.get("id")
    cotizaciones = []
    if id:
        cotizaciones = Cotizacion.objects.filter(pedido__id=id)
    context = {
        'cotizaciones':cotizaciones
    }
    return render(request, 'cotizaciones/cotizaciones.html', context)
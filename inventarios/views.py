from django.shortcuts import render
from django.http import JsonResponse
from productos.models import Producto
from .models import Inventario
from .logic.inventario_logic import get_inventario, get_producto

def inventario_list(request):
    inventario = get_inventario()
    context = {
        'inventario_list': inventario
    }
    return render(request, 'Inventario/inventarios.html', context)

def inventario_producto(request):
    codigo = request.GET.get("codigo")
    inventario = []
    if codigo:
        inventario = get_producto(int(codigo))
    context = {
        'inventario_producto':inventario
    }
    return render(request, 'Inventario/inventarios.html', context)

def consultar_stock(request):
    stock = None
    producto = None
    inventarios = Inventario.objects.all()
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            producto = Producto.objects.get(codigo=codigo)
            stock = Inventario.objects.filter(producto=producto)
        except Producto.DoesNotExist:
            stock = []
    return render(request, 'inventarios/consultar_stock.html', {
        'producto': producto,
        'stock': stock,
        'inventarios': inventarios
    })

def consultar_stock_api(request):
    """API REST para consultar stock de un producto por método GET"""
    if request.method == 'GET':
        codigo = request.GET.get('codigo')
        
        if not codigo:
            return JsonResponse({
                'error': 'Parámetro codigo es requerido',
                'message': 'Debe proporcionar el código del producto como parámetro GET'
            }, status=400)
        
        try:
            codigo = int(codigo)
            producto = Producto.objects.get(codigo=codigo)
            stock = Inventario.objects.filter(producto=producto)
            
            # Preparar datos del stock para JSON
            stock_data = []
            total_cantidad = 0
            for item in stock:
                stock_item = {
                    'id': item.id,
                    'bodega': {
                        'id': item.bodega.id,
                        'ciudad': item.bodega.ciudad,
                        'direccion': item.bodega.direccion
                    },
                    'cantidad': item.cantidad
                }
                stock_data.append(stock_item)
                total_cantidad += item.cantidad
            
            response_data = {
                'producto': {
                    'codigo': producto.codigo,
                    'nombre': producto.nombre,
                    'color': producto.color,
                    'talla': producto.talla,
                    'descripcion': producto.descripcion
                },
                'stock': stock_data,
                'resumen': {
                    'total_bodegas': len(stock_data),
                    'total_cantidad': total_cantidad
                }
            }
            
            return JsonResponse(response_data, status=200)
            
        except ValueError:
            return JsonResponse({
                'error': 'Código inválido',
                'message': 'El código debe ser un número entero válido'
            }, status=400)
        except Producto.DoesNotExist:
            return JsonResponse({
                'error': 'Producto no encontrado',
                'message': f'No existe un producto con el código {codigo}'
            }, status=404)
        except Exception as e:
            return JsonResponse({
                'error': 'Error interno del servidor',
                'message': str(e)
            }, status=500)
    
    return JsonResponse({
        'error': 'Método no permitido',
        'message': 'Solo se permite el método GET'
    }, status=405)
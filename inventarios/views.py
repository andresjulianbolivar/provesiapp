from django.shortcuts import render
from productos.models import Producto
from .models import Inventario
from .logic.inventario_logic import get_inventario

def inventario_list(request):
    inventario = get_inventario()
    context = {
        'inventario_list': inventario
    }
    return render(request, 'Inventario/inventarios.html', context)

def consultar_stock(request):
    stock = None
    producto = None
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        try:
            producto = Producto.objects.get(codigo=codigo)
            stock = Inventario.objects.filter(producto=producto)
        except Producto.DoesNotExist:
            stock = []
    return render(request, 'inventarios/consultar_stock.html', {'producto': producto, 'stock': stock})
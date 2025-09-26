from django.shortcuts import render
from .logic.inventario_logic import get_inventario

def inventario_list(request):
    inventario = get_inventario()
    context = {
        'inventario_list': inventario
    }
    return render(request, 'Inventario/inventarios.html', context)
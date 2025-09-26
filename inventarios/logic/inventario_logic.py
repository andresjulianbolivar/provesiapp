from ..models import Inventario

def get_inventario():
    queryset = Inventario.objects.all()
    return queryset

def get_producto(codigo):
    queryset = Inventario.objects.filter(producto__codigo=codigo)
    return queryset
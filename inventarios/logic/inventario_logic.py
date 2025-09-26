from ..models import Inventario

def get_inventario():
    queryset = Inventario.objects.all()
    return queryset
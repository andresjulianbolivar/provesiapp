from django.urls import path
from .views import crear_factura, crear_pedido, facturas_pendientes

urlpatterns = [
    path('crear-pedido/', crear_pedido, name='crear_pedido'),
    path('crear-factura/', crear_factura, name='crear_factura'),
    path('facturas-pendientes/', facturas_pendientes, name='facturas_pendientes'),
]

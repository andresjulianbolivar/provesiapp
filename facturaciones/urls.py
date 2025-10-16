from django.urls import path
from .views import crear_factura, facturas_pendientes

urlpatterns = [
    path('crear-factura/', crear_factura, name='crear_factura'),
    path('facturas-pendientes/', facturas_pendientes, name='facturas_pendientes'),
]

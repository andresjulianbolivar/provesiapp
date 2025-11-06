from django.urls import path
from .views import create_cotizacion, cotizaciones

urlpatterns = [
    path('crear-cotizacion/', create_cotizacion, name='crear_cotizacion'),
    path('cotizaciones/', cotizaciones, name='cotizaciones')
]

from django.urls import path
from . import views
from .views import consultar_stock

urlpatterns = [
    path('inventarios/', views.inventario_producto, name='inventarioList'),
    path('consultar-stock/', consultar_stock, name='consultar_stock'),
]

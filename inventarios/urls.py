from django.urls import path
from . import views
from .views import consultar_stock, consultar_stock_api

urlpatterns = [
    path('inventarios/', views.inventario_producto, name='inventarioList'),
    path('consultar-stock/', consultar_stock, name='consultar_stock'),
    path('api/consultar-stock/', consultar_stock_api, name='consultar_stock_api'),
]

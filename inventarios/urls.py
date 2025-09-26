from django.urls import path
from . import views

urlpatterns = [
    path('inventarios/', views.inventario_list, name='inventarioList'),
]

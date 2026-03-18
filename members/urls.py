from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pago/<int:cliente_id>/", views.registrar_pago, name="registrar_pago"),
    path("cliente/nuevo/", views.nuevo_cliente, name="nuevo_cliente"),
    path("cliente/<int:cliente_id>/editar/", views.editar_cliente, name="editar_cliente"),
    path("cliente/<int:cliente_id>/baja/", views.baja_cliente, name="baja_cliente"),
    path("cliente/<int:cliente_id>/historial/", views.historial_pagos, name="historial_pagos"),
    path("plan/crear/", views.crear_plan, name="crear_plan"),
    path("reportes/", views.reportes, name="reportes"),
]
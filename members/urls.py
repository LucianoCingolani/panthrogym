from django.urls import path
from . import views
 
urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("pago/<int:cliente_id>/", views.registrar_pago, name="registrar_pago"),
    path("cliente/nuevo/", views.nuevo_cliente, name="nuevo_cliente"),
]
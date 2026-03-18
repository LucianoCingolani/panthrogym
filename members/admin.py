from django.contrib import admin
from .models import Plan, Cliente, Pago


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("nombre", "precio", "duracion_dias")


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "plan", "telefono", "email", "activo", "fecha_inicio")
    list_filter = ("activo", "plan")
    search_fields = ("nombre", "telefono", "email")


@admin.register(Pago)
class PagoAdmin(admin.ModelAdmin):
    list_display = ("cliente", "plan", "monto", "fecha_pago")
    list_filter = ("plan",)
    search_fields = ("cliente__nombre",)
    date_hierarchy = "fecha_pago"
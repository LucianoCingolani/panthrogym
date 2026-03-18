from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta


class Plan(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=8, decimal_places=2)
    duracion_dias = models.IntegerField(default=30)

    def __str__(self):
        return f"{self.nombre} - ${self.precio}"


class Cliente(models.Model):
    nombre = models.CharField(max_length=150)
    telefono = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    activo = models.BooleanField(default=True)
    fecha_inicio = models.DateField(default=timezone.now)

    def vencimiento(self):
        ultimo = self.pagos.order_by('-fecha_pago').first()
        if ultimo:
            return ultimo.fecha_pago + relativedelta(days=self.plan.duracion_dias)
        return None

    def estado(self):
        v = self.vencimiento()
        if not v:
            return "sin_pago"
        hoy = timezone.now().date()
        if v < hoy:
            return "vencido"
        elif (v - hoy).days <= 5:
            return "por_vencer"
        return "al_dia"

    def __str__(self):
        return self.nombre


class Pago(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='pagos')
    plan = models.ForeignKey(Plan, on_delete=models.SET_NULL, null=True)
    monto = models.DecimalField(max_digits=8, decimal_places=2)
    fecha_pago = models.DateField(default=timezone.now)
    nota = models.CharField(max_length=200, blank=True)

    class Meta:
        ordering = ['-fecha_pago']

    def __str__(self):
        return f"{self.cliente} - {self.fecha_pago}"
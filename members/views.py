from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Cliente, Plan, Pago


def dashboard(request):
    clientes = Cliente.objects.filter(activo=True).select_related('plan')

    orden = {"vencido": 0, "por_vencer": 1, "sin_pago": 2, "al_dia": 3}
    clientes_ordenados = sorted(clientes, key=lambda c: orden[c.estado()])

    resumen = {
        "vencidos":   sum(1 for c in clientes if c.estado() == "vencido"),
        "por_vencer": sum(1 for c in clientes if c.estado() == "por_vencer"),
        "al_dia":     sum(1 for c in clientes if c.estado() == "al_dia"),
        "total":      clientes.count(),
    }

    return render(request, "dashboard.html", {
        "clientes": clientes_ordenados,
        "resumen": resumen,
    })


def registrar_pago(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
 
    if request.method == "POST":
        fecha = request.POST.get("fecha_pago") or timezone.now().date()
        Pago.objects.create(
            cliente=cliente,
            plan=cliente.plan,
            monto=cliente.plan.precio,
            fecha_pago=fecha,
        )
        return redirect("dashboard")
 
    return render(request, "confirmar_pago.html", {
        "cliente": cliente,
        "hoy": timezone.now().date().isoformat(),
    })


def nuevo_cliente(request):
    planes = Plan.objects.all()

    if request.method == "POST":
        Cliente.objects.create(
            nombre=request.POST["nombre"],
            telefono=request.POST.get("telefono", ""),
            email=request.POST.get("email", ""),
            plan=get_object_or_404(Plan, pk=request.POST["plan"]),
        )
        return redirect("dashboard")

    return render(request, "nuevo_cliente.html", {"planes": planes})
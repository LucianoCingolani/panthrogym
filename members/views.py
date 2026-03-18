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

def crear_plan(request):
    if request.method == "POST":
        Plan.objects.create(
            nombre=request.POST["nombre"],
            precio=request.POST["precio"],
            duracion_dias=request.POST.get("duracion_dias", 30),
        )
    return redirect(request.POST.get("next", "dashboard"))

def editar_cliente(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    planes = Plan.objects.all()
 
    if request.method == "POST":
        cliente.nombre = request.POST["nombre"]
        cliente.telefono = request.POST.get("telefono", "")
        cliente.email = request.POST.get("email", "")
        cliente.plan = get_object_or_404(Plan, pk=request.POST["plan"])
        cliente.save()
        return redirect("dashboard")
 
    return render(request, "editar_cliente.html", {
        "cliente": cliente,
        "planes": planes,
    })
 

def baja_cliente(request, cliente_id):
    if request.method == "POST":
        cliente = get_object_or_404(Cliente, pk=cliente_id)
        cliente.activo = False
        cliente.save()
    return redirect("dashboard")

def historial_pagos(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    pagos = cliente.pagos.select_related('plan').order_by('-fecha_pago')
    return render(request, "historial_pagos.html", {
        "cliente": cliente,
        "pagos": pagos,
    })

def reportes(request):
    from django.db.models import Sum
    from datetime import date
 
    hoy = date.today()
    mes = int(request.GET.get("mes", hoy.month))
    anio = int(request.GET.get("anio", hoy.year))
 
    pagos_mes = Pago.objects.filter(
        fecha_pago__year=anio,
        fecha_pago__month=mes,
    ).select_related('cliente', 'plan').order_by('-fecha_pago')
 
    total_recaudado = pagos_mes.aggregate(total=Sum('monto'))['total'] or 0
 
    clientes_activos = Cliente.objects.filter(activo=True)
    no_renovaron = [c for c in clientes_activos if not c.pagos.filter(
        fecha_pago__year=anio, fecha_pago__month=mes
    ).exists()]
 
    return render(request, "reportes.html", {
        "pagos_mes": pagos_mes,
        "total_recaudado": total_recaudado,
        "no_renovaron": no_renovaron,
        "mes": mes,
        "anio": anio,
        "hoy": hoy,
    })
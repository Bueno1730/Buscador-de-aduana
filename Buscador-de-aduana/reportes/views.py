from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import ReporteError
from .forms import ReporteErrorForm

def reportar_error(request):
    if request.method == 'POST':
        form = ReporteErrorForm(request.POST, request.FILES)
        if form.is_valid():
            reporte = form.save(commit=False)
            if request.user.is_authenticated:
                reporte.usuario = request.user
                reporte.es_usuario_registrado = True
            reporte.save()
            messages.success(request, '¡Reporte enviado exitosamente!')
            return redirect('reportes:confirmacion', reporte_id=reporte.id)
    else:
        form = ReporteErrorForm()
    return render(request, 'reportes/reportar_error.html', {'form': form})

def confirmacion_reporte(request, reporte_id):
    reporte = get_object_or_404(ReporteError, id=reporte_id)
    return render(request, 'reportes/confirmacion.html', {'reporte': reporte})

@login_required
def mis_reportes(request):
    reportes = ReporteError.objects.filter(usuario=request.user)
    return render(request, 'reportes/mis_reportes.html', {'reportes': reportes})

@staff_member_required
def lista_reportes_admin(request):
    reportes = ReporteError.objects.all()
    estado = request.GET.get('estado')
    categoria = request.GET.get('categoria')
    if estado:
        reportes = reportes.filter(estado=estado)
    if categoria:
        reportes = reportes.filter(categoria=categoria)
    return render(request, 'reportes/admin_lista.html', {'reportes': reportes})

@staff_member_required
def detalle_reporte_admin(request, reporte_id):
    reporte = get_object_or_404(ReporteError, id=reporte_id)
    if request.method == 'POST':
        reporte.estado = request.POST.get('estado', reporte.estado)
        reporte.prioridad = request.POST.get('prioridad', reporte.prioridad)
        reporte.notas_admin = request.POST.get('notas_admin', reporte.notas_admin)
        reporte.save()
        messages.success(request, 'Reporte actualizado.')
        return redirect('reportes:admin_detalle', reporte_id=reporte.id)
    return render(request, 'reportes/admin_detalle.html', {'reporte': reporte})
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils import timezone
from datetime import timedelta
from .models import ReporteError
from .forms import ReporteErrorForm

def puede_modificar(reporte):
    return timezone.now() - reporte.fecha_creacion < timedelta(minutes=10)

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
            messages.warning(request, 'Tienes 10 minutos para hacer modificaciones o eliminar tu reporte.')
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

@login_required
def detalle_reporte_usuario(request, reporte_id):
    reporte = get_object_or_404(ReporteError, id=reporte_id, usuario=request.user)
    puede_editar = puede_modificar(reporte)
    return render(request, 'reportes/detalle_reporte_usuario.html', {
        'reporte': reporte, 'puede_editar': puede_editar
    })

@login_required
def editar_reporte(request, reporte_id):
    reporte = get_object_or_404(ReporteError, id=reporte_id, usuario=request.user)
    if not puede_modificar(reporte):
        messages.error(request, 'El tiempo de edición ha expirado (10 minutos).')
        return redirect('reportes:detalle_usuario', reporte_id=reporte.id)
    if request.method == 'POST':
        form = ReporteErrorForm(request.POST, request.FILES, instance=reporte)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reporte actualizado correctamente.')
            return redirect('reportes:detalle_usuario', reporte_id=reporte.id)
    else:
        form = ReporteErrorForm(instance=reporte)
    return render(request, 'reportes/editar_reporte.html', {'form': form, 'reporte': reporte})

@login_required
def eliminar_reporte(request, reporte_id):
    reporte = get_object_or_404(ReporteError, id=reporte_id, usuario=request.user)
    if not puede_modificar(reporte):
        messages.error(request, 'El tiempo de edición ha expirado (10 minutos).')
        return redirect('reportes:detalle_usuario', reporte_id=reporte.id)
    if request.method == 'POST':
        reporte.delete()
        messages.success(request, 'Reporte eliminado correctamente.')
        return redirect('reportes:mis_reportes')
    return render(request, 'reportes/confirmar_eliminar.html', {'reporte': reporte})

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
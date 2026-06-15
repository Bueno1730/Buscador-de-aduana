from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import ReferenciaClasificacion
from .forms import BusquedaReferenciaForm


@login_required
def lista_referencias(request):
    form = BusquedaReferenciaForm(request.GET)
    referencias = ReferenciaClasificacion.objects.all()

    if form.is_valid():
        texto = form.cleaned_data.get('texto')
        tipo = form.cleaned_data.get('tipo')
        codigo = form.cleaned_data.get('codigo_arancelario')

        if texto:
            referencias = referencias.filter(
                Q(titulo__icontains=texto) | Q(descripcion__icontains=texto)
            )
        if tipo:
            referencias = referencias.filter(tipo=tipo)
        if codigo:
            referencias = referencias.filter(
                codigos_arancelarios__codigo__icontains=codigo
            ).distinct()

    return render(request, 'referencias/lista_referencias.html', {
        'form': form,
        'referencias': referencias,
    })


@login_required
def detalle_referencia(request, referencia_id):
    referencia = get_object_or_404(ReferenciaClasificacion, id=referencia_id)
    return render(request, 'referencias/detalle_referencia.html', {
        'referencia': referencia,
    })

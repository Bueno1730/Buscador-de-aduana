from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from .models import Arancel, HistorialBusqueda
from .forms import ArancelForm

@login_required
@never_cache
def home(request):
    return render(request, 'home.html')

@login_required
@never_cache
def vista_busqueda(request):
    query = request.GET.get('codigo')
    resultados = None

    if query: # Volvemos a buscar solo con el código
        resultados = Arancel.objects.filter(codigo__icontains=query)
        
        # Guardamos el historial de forma invisible y automática
        HistorialBusqueda.objects.create(
            usuario=request.user,
            codigo_buscado=query
        )

    return render(request, 'busqueda.html', {'resultados': resultados, 'query': query})

@staff_member_required # Candado: Solo administradores pueden ver la auditoría
def auditoria_busquedas(request):
    # Traemos todo el historial (ya viene ordenado por fecha gracias al Meta del modelo)
    registros = HistorialBusqueda.objects.all()
    return render(request, 'auditoria.html', {'registros': registros})

@staff_member_required
@never_cache
def agregar_arancel(request):
    if request.method == 'POST':
        form = ArancelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Partida arancelaria guardada correctamente!')
            return redirect('agregar_arancel')
    else:
        form = ArancelForm()
    
    return render(request, 'agregar_arancel.html', {'form': form})
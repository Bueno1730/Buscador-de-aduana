from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from .models import Arancel
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

    if query:
        resultados = Arancel.objects.filter(codigo__icontains=query)

    return render(request, 'busqueda.html', {'resultados': resultados})

@staff_member_required
@never_cache
def agregar_arancel(request):
    if request.method == 'POST':
        form = ArancelForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Partida arancelaria guardada correctamente!')
            return redirect('busqueda')
    else:
        form = ArancelForm()
    
    return render(request, 'agregar_arancel.html', {'form': form})
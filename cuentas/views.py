from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Arancel

@login_required
def home(request):
    return render(request, 'home.html')

@login_required # <-- Añade esto para proteger el buscador
def vista_busqueda(request):
    query = request.GET.get('codigo')
    resultados = None

    if query:
        resultados = Arancel.objects.filter(codigo__icontains=query)

    return render(request, 'busqueda.html', {'resultados': resultados})
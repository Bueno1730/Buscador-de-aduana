from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Arancel  # <-- Importamos tu modelo de base de datos

@login_required
def home(request):
    return render(request, 'home.html')

def vista_busqueda(request):
    # 1. Atrapamos lo que el usuario escribió en la barra de búsqueda
    query = request.GET.get('codigo')
    resultados = None

    # 2. Si el usuario escribió algo, filtramos la base de datos
    if query:
        # 'icontains' permite buscar coincidencias parciales (ej: buscar "0101" traerá todo lo que empiece o contenga 0101)
        resultados = Arancel.objects.filter(codigo__icontains=query)

    # 3. Enviamos la lista de resultados a tu diseño HTML
    return render(request, 'busqueda.html', {'resultados': resultados})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    return render(request, 'home.html')

# Añadimos la nueva vista del buscador aquí abajo:
def vista_busqueda(request):
    return render(request, 'busqueda.html')
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from .models import Arancel, HistorialBusqueda
from .forms import ArancelForm
from django.db.models import Q

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
        # MAGIA AQUÍ: Buscamos en el código O en la descripción (ignorando mayúsculas/minúsculas)
        resultados = Arancel.objects.filter(
            Q(codigo__icontains=query) | Q(descripcion__icontains=query)
        )
        
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

# ==========================================
# NUEVA VISTA: Detalles del Arancel
# ==========================================
@login_required
def detalle_arancel(request, arancel_id):
    # Busca el arancel por su ID único, si no existe lanza un error 404
    arancel = get_object_or_404(Arancel, id=arancel_id)
    return render(request, 'detalle_arancel.html', {'arancel': arancel})

@login_required
@never_cache
def editar_arancel(request, arancel_id):
    # Criterio 2: Bloqueo de URL directo para usuarios no administradores (Despachantes)
    if not request.user.is_staff:
        messages.error(request, "Acceso denegado. No tienes permisos para realizar esta acción.")
        return redirect('home') # O redirige a 'vista_busqueda' si prefieres

    # Busca el arancel a editar
    arancel = get_object_or_404(Arancel, id=arancel_id)

    if request.method == 'POST':
        # Criterio 3 y 4: Pre-carga los datos (instance) y valida los campos requeridos
        form = ArancelForm(request.POST, instance=arancel)
        if form.is_valid():
            form.save()
            # Criterio 3: Mensaje de éxito exacto según la historia de usuario
            messages.success(request, "Información arancelaria actualizada correctamente.")
            return redirect('detalle_arancel', arancel_id=arancel.id)
    else:
        # Cargar el formulario con la información actual de la base de datos
        form = ArancelForm(instance=arancel)
    
    return render(request, 'editar_arancel.html', {'form': form, 'arancel': arancel})
import os
import re
import tablib
from dotenv import load_dotenv
import google.generativeai as genai
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.cache import never_cache
from django.contrib.auth.models import User
from .models import Arancel, HistorialBusqueda
from .forms import ArancelForm
from django.db.models import Q
from .admin import ArancelResource

# ==========================================
# CONFIGURACIÓN DE LA IA (A prueba de fallos)
# ==========================================
# 1. Intentar cargar el archivo .env
load_dotenv()

# 2. Obtener la clave de forma segura
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# 3. Configurar Gemini SOLO si la clave existe
modelo_ia = None
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    modelo_ia = genai.GenerativeModel('gemini-2.5-flash')


@login_required
@never_cache
def home(request):
    return render(request, 'home.html')


@login_required
@never_cache
def vista_busqueda(request):
    # 1. Capturar los 5 cuadros de dígitos
    box1 = request.GET.get('box1', '').strip()
    box2 = request.GET.get('box2', '').strip()
    box3 = request.GET.get('box3', '').strip()
    box4 = request.GET.get('box4', '').strip()
    box5 = request.GET.get('box5', '').strip()
    
    # 2. Capturar la búsqueda por palabra clave y el capítulo seleccionado
    texto_buscar = request.GET.get('texto_buscar', '').strip()
    capitulo_seleccionado = request.GET.get('capitulo', '').strip()
    
    resultados = None

    # Mantenemos la lista para el filtro desplegable
    todos_los_codigos = Arancel.objects.values_list('codigo', flat=True)
    capitulos_disponibles = sorted(list(set([cod[:2] for cod in todos_los_codigos if cod and len(cod) >= 2])))

    # 3. Construcción inteligente del código arancelario
    codigo_construido = ""
    if box1:
        codigo_construido += box1
        if box2:
            codigo_construido += box2
            if box3:
                codigo_construido += "." + box3
                if box4:
                    codigo_construido += "." + box4
                    if box5:
                        codigo_construido += "." + box5

    # 4. Aplicar los filtros combinados
    if codigo_construido or texto_buscar:
        resultados = Arancel.objects.all()
        
        # Filtro por estructura de código numérico
        if codigo_construido:
            resultados = resultados.filter(codigo__startswith=codigo_construido)
            
        # Filtro por texto en la descripción
        if texto_buscar:
            resultados = resultados.filter(descripcion__icontains=texto_buscar)
            
            # El capítulo se aplica SOLO si hay texto_buscar y no hay código numérico
            if capitulo_seleccionado and not codigo_construido:
                resultados = resultados.filter(codigo__startswith=capitulo_seleccionado)
        
        # Guardar en el historial
        termino_historial = f"{codigo_construido} | {texto_buscar}".strip(" | ")
        if capitulo_seleccionado and not codigo_construido:
            termino_historial += f" (Capítulo: {capitulo_seleccionado})"
            
        HistorialBusqueda.objects.create(
            usuario=request.user,
            codigo_buscado=termino_historial
        )

    return render(request, 'busqueda.html', {
        'resultados': resultados,
        'box1': box1,
        'box2': box2,
        'box3': box3,
        'box4': box4,
        'box5': box5,
        'texto_buscar': texto_buscar,
        'capitulo_seleccionado': capitulo_seleccionado,
        'capitulos_disponibles': capitulos_disponibles
    })
    
    
@staff_member_required
def auditoria_busquedas(request):
    usuarios = User.objects.filter(historialbusqueda__isnull=False).distinct()
    usuario_filtro = request.GET.get('usuario', '')

    registros = HistorialBusqueda.objects.all()
    if usuario_filtro:
        registros = registros.filter(usuario__username=usuario_filtro)

    return render(request, 'auditoria.html', {
        'registros': registros,
        'usuarios': usuarios,
        'usuario_filtro': usuario_filtro,
    })


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


@login_required
def detalle_arancel(request, arancel_id):
    arancel = get_object_or_404(Arancel, id=arancel_id)
    return render(request, 'detalle_arancel.html', {'arancel': arancel})


@login_required
@never_cache
def editar_arancel(request, arancel_id):
    if not request.user.is_staff:
        messages.error(request, "Acceso denegado. No tienes permisos para realizar esta acción.")
        return redirect('home')

    arancel = get_object_or_404(Arancel, id=arancel_id)

    if request.method == 'POST':
        form = ArancelForm(request.POST, instance=arancel)
        if form.is_valid():
            form.save()
            messages.success(request, "Información arancelaria actualizada correctamente.")
            return redirect('detalle_arancel', arancel_id=arancel.id)
    else:
        form = ArancelForm(instance=arancel)
    
    return render(request, 'editar_arancel.html', {'form': form, 'arancel': arancel})


@staff_member_required
def carga_masiva(request):
    if request.method == 'POST':
        archivo = request.FILES.get('archivo')

        if not archivo:
            messages.error(request, "Por favor selecciona un archivo.")
            return redirect('carga_masiva')

        formato = archivo.name.split('.')[-1].lower()
        if formato not in ['csv', 'xlsx']:
            messages.error(request, "Formato no válido. Usa archivos .csv o .xlsx")
            return redirect('carga_masiva')

        dataset = tablib.Dataset()
        try:
            if formato == 'csv':
                dataset.load(archivo.read().decode('utf-8'), format='csv')
            else:
                dataset.load(archivo.read(), format='xlsx')

            arancel_resource = ArancelResource()
            resultado = arancel_resource.import_data(dataset, dry_run=True)

            if not resultado.has_errors():
                arancel_resource.import_data(dataset, dry_run=False)
                messages.success(request, f"¡Se importaron los aranceles correctamente!")
                return redirect('home')
            else:
                messages.error(request, "El archivo tiene errores o columnas faltantes. Revisa tu Excel.")
                
        except Exception as e:
            messages.error(request, f"Error al leer el archivo: Comprueba el formato.")

    return render(request, 'carga_masiva.html')


@login_required
def pantalla_chat(request):
    return render(request, 'chat.html')


# ==========================================
# NUEVA VISTA: CHAT INTELIGENTE (VERSIÓN FINAL COMPLETA)
# ==========================================
@login_required
def chat_inteligente(request):
    if request.method == 'POST':
        
        # --- VALIDACIÓN DE DEGRADACIÓN ELEGANTE ---
        if not modelo_ia:
            mensaje_ayuda = (
                "⚠️ **Aviso del Sistema:**\n"
                "Hola, soy Sisa. Para poder responderte, necesito que configures mi motor de Inteligencia Artificial.\n\n"
                "**Instrucciones para desarrolladores:**\n"
                "1. Crea un archivo `.env` en la raíz del proyecto.\n"
                "2. Añade la variable `GEMINI_API_KEY=tu_clave_aqui`.\n"
                "3. Reinicia el servidor de Django."
            )
            return JsonResponse({'respuesta': mensaje_ayuda})

        pregunta_usuario = request.POST.get('pregunta', '').strip()

        if not pregunta_usuario:
            return JsonResponse({'respuesta': 'Por favor, escribe una pregunta.'})

        # 1. LIMPIEZA DE LA PREGUNTA
        pregunta_limpia = re.sub(r'[^\w\s]', '', pregunta_usuario.lower())
        
        palabras_basura = [
            'qué', 'que', 'cuál', 'cual', 'cómo', 'como', 'cuánto', 'cuanto', 'cuales',
            'tiene', 'tienen', 'para', 'con', 'los', 'las', 'una', 'unos', 'un', 'el', 'la',
            'arancel', 'aranceles', 'importacion', 'importar', 'exportacion', 'exportar',
            'paga', 'pagan', 'documentos', 'documento', 'presenta', 'presentar',
            'necesita', 'necesitan', 'necesito', 'nesesito', 'requisitos', 'requisito',
            'del', 'de', 'sobre', 'se', 'en', 'por', 'son', 'es', 'legal', 'disposicion',
            'unidad', 'medida', 'esta', 'estan'
        ]
        
        palabras_clave = [p for p in pregunta_limpia.split() if p not in palabras_basura and len(p) > 2]

        # 2. BÚSQUEDA LOCAL JERÁRQUICA (PADRES E HIJOS)
        resultados_db = Arancel.objects.none()
        
        if palabras_clave:
            consulta_base = Q()
            for palabra in palabras_clave:
                consulta_base |= (
                    Q(descripcion__icontains=palabra) | 
                    Q(codigo__icontains=palabra)
                )
            
            matches_iniciales = Arancel.objects.filter(consulta_base)
            
            raices = set()
            for match in matches_iniciales[:5]:
                codigo_limpio = match.codigo.replace('.', '')
                if len(codigo_limpio) >= 4:
                    raices.add(codigo_limpio[:4])
            
            if raices:
                consulta_familia = Q()
                for raiz in raices:
                    formato_padre = f"{raiz[:2]}.{raiz[2:]}"
                    formato_hijo = raiz
                    consulta_familia |= Q(codigo__startswith=formato_padre) | Q(codigo__startswith=formato_hijo)
                
                resultados_db = Arancel.objects.filter(consulta_familia).order_by('codigo')[:25]
            else:
                resultados_db = matches_iniciales[:5]

        # 3. ARMAR EL CONTEXTO ESTRICTO (CON TODOS LOS DATOS)
        if resultados_db.exists():
            contexto_arancelario = "Datos encontrados en la base de datos oficial:\n"
            for item in resultados_db:
                ga_texto = item.ga_porcentaje if item.ga_porcentaje else "-"
                ice_texto = item.ice_iehd if item.ice_iehd else "-"
                u_medida = item.unidad_medida if item.unidad_medida else "No especificada"
                doc_texto = item.doc_tipo if item.doc_tipo else "Ninguno"
                entidad_texto = item.doc_entidad if item.doc_entidad else "-"
                disp_texto = item.doc_disposicion if item.doc_disposicion else "-"
                
                contexto_arancelario += (
                    f"- Partida: {item.codigo} | "
                    f"Desc: {item.descripcion} | "
                    f"GA: {ga_texto}% | "
                    f"ICE: {ice_texto} | "
                    f"Unidad de Medida: {u_medida} | "
                    f"Doc: {doc_texto} (Entidad: {entidad_texto}, Ley: {disp_texto})\n"
                )
        else:
            contexto_arancelario = "No se encontraron datos en la base."

        # 4. EL PROMPT MAESTRO
        prompt_maestro = f"""
        Eres un asistente experto en aduanas exclusivo para el sistema SISARM.
        
        REGLAS ESTRICTAS:
        1. Responde ÚNICAMENTE basándote en la sección 'Datos encontrados'.
        2. La nomenclatura es jerárquica: las partidas generales (ej. 01.01) tienen subpartidas específicas. Desglosa las opciones si la pregunta es general.
        3. Si un dato marca '-', significa que la base de datos no tiene ese valor asignado.
        4. Sé claro, directo y usa viñetas para que sea fácil de leer.
        
        {contexto_arancelario}
        
        Pregunta del usuario: {pregunta_usuario}
        """

        # 5. LLAMAR A LA IA
        try:
            respuesta_ia = modelo_ia.generate_content(prompt_maestro)
            texto_respuesta = respuesta_ia.text
        except Exception as e:
            texto_respuesta = "Hubo un error al intentar conectar con el motor de Inteligencia Artificial."

        return JsonResponse({'respuesta': texto_respuesta})

    return JsonResponse({'error': 'Método no permitido'}, status=405)
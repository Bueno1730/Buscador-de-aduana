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
from .forms import UsuarioPersonalForm
from django.urls import reverse
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
# NUEVA VISTA: CHAT INTELIGENTE (VERSIÓN DEFINITIVA CON MEMORIA)
# ==========================================
@login_required
def chat_inteligente(request):
    if request.method == 'POST':
        
        # --- VALIDACIÓN DE DEGRADACIÓN ELEGANTE ---
        if not modelo_ia:
            return JsonResponse({'respuesta': "⚠️ **Aviso:** El motor de IA no está configurado (falta API Key)."})

        # 1. RECIBIR DATOS Y MEMORIA DEL FRONTEND
        pregunta_usuario = request.POST.get('pregunta', '').strip()
        memoria_chat = request.POST.get('memoria_chat', '').strip()
        ultima_pregunta = request.POST.get('ultima_pregunta', '').strip()

        if not pregunta_usuario:
            return JsonResponse({'respuesta': 'Por favor, escribe una pregunta.'})

        # 2. LIMPIEZA DE LA PREGUNTA (Combinando historial para buscar en la BD)
        texto_busqueda = f"{ultima_pregunta} {pregunta_usuario}".lower()
        pregunta_limpia = re.sub(r'[^\w\s]', '', texto_busqueda)
        
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

        # 3. BÚSQUEDA LOCAL JERÁRQUICA (PADRES E HIJOS)
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

        # 4. ARMAR EL CONTEXTO ESTRICTO (AQUÍ SE CREA LA VARIABLE QUE FALTABA)
        if resultados_db.exists():
            contexto_arancelario = "Datos encontrados en la base de datos oficial:\n"
            for item in resultados_db:
                ga_texto = item.ga_porcentaje if item.ga_porcentaje else "-"
                ice_texto = item.ice_iehd if item.ice_iehd else "-"
                doc_texto = item.doc_tipo if item.doc_tipo else "Ninguno"
                
                url_detalle = reverse('detalle_arancel', args=[item.id])
                
                contexto_arancelario += (
                    f"- Partida: {item.codigo} (URL_BOTON: {url_detalle}) | "
                    f"Desc: {item.descripcion} | "
                    f"GA: {ga_texto}% | "
                    f"ICE: {ice_texto} | "
                    f"Doc: {doc_texto}\n"
                )
        else:
            contexto_arancelario = "No se encontraron datos en la base."

        # 5. EL PROMPT MAESTRO (CON MEMORIA INCLUIDA)
        prompt_maestro = f"""
        Eres Sisa, un asistente experto en aduanas exclusivo para el sistema SISARM.
        
        REGLAS ESTRICTAS DE FORMATO Y COMPORTAMIENTO (CRÍTICO):
        1. Presenta la información siempre en listas o viñetas cortas. NUNCA uses párrafos largos.
        2. Resalta SIEMPRE en **negrita** los valores clave, por ejemplo: **GA: 10%** o **ICE: 5%**.
        3. Cuando menciones una partida arancelaria específica, DEBES colocar un enlace en formato Markdown al final de la explicación usando la 'URL_BOTON' proporcionada en el contexto. 
           Formato exacto obligatorio: [🔍 Ver Detalle Completo](/la/url/proporcionada/)
        4. No inventes URLs, usa únicamente la que se te entrega en los datos.
        5. REGLA DE AMBIGÜEDAD: Si la pregunta del usuario es general o hay múltiples variantes, NO des una lista larga. Haz una pregunta amigable para acotar la búsqueda sugiriendo opciones.
        
        HISTORIAL DE LA CONVERSACIÓN RECIENTE:
        {memoria_chat if memoria_chat else "Esta es la primera interacción del usuario, no hay historial previo."}
        
        DATOS ENCONTRADOS EN LA BASE DE DATOS OFICIAL:
        {contexto_arancelario}
        
        Pregunta actual del usuario: {pregunta_usuario}
        """

        # 6. LLAMAR A LA IA
        try:
            print("🚀 Enviando prompt a Gemini con memoria...") 
            respuesta_ia = modelo_ia.generate_content(prompt_maestro)
            texto_respuesta = respuesta_ia.text
        except Exception as e:
            error_msg = f"❌ Error técnico de IA: {str(e)}"
            print(error_msg)
            return JsonResponse({'respuesta': error_msg})

        return JsonResponse({'respuesta': texto_respuesta})

    return JsonResponse({'error': 'Método no permitido'}, status=405)
# ==========================================
# GESTIÓN DE PERSONAL (CRUD)
# ==========================================


@staff_member_required
@never_cache
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    return render(request, 'usuarios/lista.html', {'usuarios': usuarios})

@staff_member_required
@never_cache
def crear_usuario(request):
    if request.method == 'POST':
        form = UsuarioPersonalForm(request.POST)
        if form.is_valid():
            # Validar que al crear un usuario nuevo, la contraseña no esté vacía
            if not form.cleaned_data.get('password'):
                form.add_error('password', 'La contraseña es obligatoria para un usuario nuevo.')
            else:
                form.save()
                messages.success(request, "Cuenta de personal creada y habilitada exitosamente.")
                return redirect('lista_usuarios')
    else:
        form = UsuarioPersonalForm()
    
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Registrar Nuevo Personal'})

@staff_member_required
@never_cache
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UsuarioPersonalForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Datos del personal actualizados.")
            return redirect('lista_usuarios')
    else:
        # Pre-seleccionar el rol actual del usuario en el desplegable
        rol_actual = 'administrador' if usuario.is_staff else 'despachante'
        form = UsuarioPersonalForm(instance=usuario, initial={'rol': rol_actual})
        
    return render(request, 'usuarios/form.html', {'form': form, 'titulo': 'Editar Personal'})

@staff_member_required
def eliminar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        if usuario == request.user:
            messages.error(request, "Por seguridad, no puedes eliminar tu propia cuenta de administrador.")
        else:
            usuario.delete()
            messages.success(request, "Cuenta eliminada del sistema.")
        return redirect('lista_usuarios')
    
    return render(request, 'usuarios/confirmar_eliminar.html', {'usuario': usuario})
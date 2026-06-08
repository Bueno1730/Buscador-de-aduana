from django.contrib import admin
from django import forms
import re
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Arancel
from django.contrib import messages

# --- REGLAS DE VALIDACIÓN DE LA HISTORIA DE USUARIO ---
class ArancelForm(forms.ModelForm):
    class Meta:
        model = Arancel
        fields = '__all__'

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')
        
        # Criterio 2: Validación de formato (Números, puntos, guiones y letras mayúsculas permitidas según tu regex)
        if codigo and not re.match(r'^[0-9\.\-A-Z]+$', codigo):
            raise forms.ValidationError("El código debe contener únicamente caracteres válidos para el arancel.")
        
        # Criterio 3: Prevención de códigos duplicados
        # Verificamos si estamos creando un registro nuevo y si ese código ya existe
        if not self.instance.pk and Arancel.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("Este código arancelario ya se encuentra registrado en el sistema.")
            
        return codigo

# --- CONFIGURACIÓN DE IMPORTACIÓN MASIVA (EL MAPA DEL EXCEL) ---
class ArancelResource(resources.ModelResource):
    class Meta:
        model = Arancel
        import_id_fields = ('codigo',) 
        # Aquí le decimos exactamente cuáles son las 13 columnas que debe leer de tu Excel
        fields = (
            'codigo', 
            'descripcion', 
            'notas_explicativas',
            'ga_porcentaje', 
            'ice_iehd', 
            'unidad_medida', 
            'despacho_frontera', 
            'doc_tipo', 
            'doc_entidad', 
            'doc_disposicion', 
            'pref_can_ace', 
            'pref_ace22_chi', 
            'pref_ace22_prot', 
            'pref_ace66_mexico'
        )

# --- PANEL DE ADMINISTRACIÓN ---
@admin.register(Arancel)
class ArancelAdmin(ImportExportModelAdmin):
    resource_classes = [ArancelResource]
    form = ArancelForm # Conectamos tus validaciones
    list_display = ('codigo', 'descripcion', 'ga_porcentaje', 'unidad_medida')
    search_fields = ('codigo', 'descripcion')

    # Criterio 1: Mensaje de éxito personalizado al guardar
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if not change: # Si es una creación nueva y no una edición
            messages.success(request, "Partida arancelaria guardada correctamente.")


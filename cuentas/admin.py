from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from .models import Arancel

# Definimos cómo se importarán los datos
class ArancelResource(resources.ModelResource):
    class Meta:
        model = Arancel
        # Le decimos que el 'codigo' es la llave principal (no se repetirá)
        import_id_fields = ('codigo',) 

# Integramos la carga masiva en el panel
@admin.register(Arancel)
class ArancelAdmin(ImportExportModelAdmin):
    resource_classes = [ArancelResource] # Conectamos la configuración anterior
    list_display = ('codigo', 'descripcion', 'ga_porcentaje', 'unidad_medida')
    search_fields = ('codigo', 'descripcion')
from django.contrib import admin
from .models import ReferenciaClasificacion


@admin.register(ReferenciaClasificacion)
class ReferenciaClasificacionAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tipo', 'entidad_emisora', 'fecha_emision')
    list_filter = ('tipo', 'entidad_emisora')
    search_fields = ('titulo', 'descripcion')
    filter_horizontal = ('codigos_arancelarios',)

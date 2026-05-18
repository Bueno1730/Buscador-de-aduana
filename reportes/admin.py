from django.contrib import admin
from .models import ReporteError

@admin.register(ReporteError)
class ReporteErrorAdmin(admin.ModelAdmin):
    list_display = ['id', 'titulo', 'categoria', 'estado', 'prioridad', 'nombre_reportante', 'fecha_creacion']
    list_filter = ['estado', 'categoria', 'prioridad']
    search_fields = ['titulo', 'descripcion', 'email_reportante']
    list_editable = ['estado', 'prioridad']
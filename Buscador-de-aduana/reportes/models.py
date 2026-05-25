from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ReporteError(models.Model):
    CATEGORIAS = [
        ('partida_arancelaria', 'Error en Partida Arancelaria'),
        ('codigo_producto', 'Error en Código de Producto'),
        ('tarifa', 'Error en Tarifa/Arancel'),
        ('descripcion', 'Error en Descripción'),
        ('busqueda', 'Error en Búsqueda'),
        ('visualizacion', 'Error de Visualización'),
        ('otro', 'Otro'),
    ]
    
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('en_revision', 'En Revisión'),
        ('resuelto', 'Resuelto'),
        ('rechazado', 'Rechazado'),
    ]
    
    PRIORIDADES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    titulo = models.CharField(max_length=200)
    categoria = models.CharField(max_length=50, choices=CATEGORIAS, default='otro')
    descripcion = models.TextField()
    
    partida_arancelaria_afectada = models.CharField(max_length=20, blank=True, null=True)
    codigo_producto_afectado = models.CharField(max_length=50, blank=True, null=True)
    
    captura_pantalla = models.ImageField(upload_to='reportes_errores/capturas/%Y/%m/', blank=True, null=True)
    
    nombre_reportante = models.CharField(max_length=100)
    email_reportante = models.EmailField()
    es_usuario_registrado = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    prioridad = models.CharField(max_length=20, choices=PRIORIDADES, default='media')
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    fecha_resolucion = models.DateTimeField(null=True, blank=True)
    notas_admin = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f"{self.titulo} - {self.get_estado_display()}"
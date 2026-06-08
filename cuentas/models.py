from django.db import models
from django.contrib.auth.models import User

class Arancel(models.Model):
    # Código arancelario (ej: '0101.21.00.00'). Usamos CharField por los puntos.
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    descripcion = models.TextField(verbose_name="Descripción de la Mercancía")
    notas_explicativas = models.TextField(null=True, blank=True, verbose_name="Notas Explicativas y Legales")
    
    # Gravamen Arancelario (GA %)
    ga_porcentaje = models.IntegerField(null=True, blank=True, verbose_name="GA %")
    
    # Impuestos adicionales
    ice_iehd = models.CharField(max_length=50, null=True, blank=True, verbose_name="ICE - IEHD")
    unidad_medida = models.CharField(max_length=10, null=True, blank=True, verbose_name="Unidad de Medida")
    despacho_frontera = models.CharField(max_length=100, null=True, blank=True, verbose_name="Despacho en Frontera")
    
    # Documento Adicional para el Despacho
    doc_tipo = models.CharField(max_length=20, null=True, blank=True, verbose_name="Tipo de Doc")
    doc_entidad = models.CharField(max_length=100, null=True, blank=True, verbose_name="Entidad que emite")
    doc_disposicion = models.CharField(max_length=150, null=True, blank=True, verbose_name="Disp. Legal")
    
    # Preferencias Arancelarias
    pref_can_ace = models.CharField(max_length=20, null=True, blank=True, verbose_name="CAN/ACE36/ACE47/VEN")
    pref_ace22_chi = models.CharField(max_length=20, null=True, blank=True, verbose_name="ACE 22 Chi")
    pref_ace22_prot = models.CharField(max_length=20, null=True, blank=True, verbose_name="ACE 22 Prot")
    pref_ace66_mexico = models.CharField(max_length=20, null=True, blank=True, verbose_name="ACE 66 México")

    def __str__(self):
        return f"{self.codigo} - {self.descripcion[:30]}..."

    class Meta:
        verbose_name = "Arancel"
        verbose_name_plural = "Aranceles"

# =========================================================
# NUEVA CLASE: Debe estar alineada a la izquierda (0 espacios)
# =========================================================
class HistorialBusqueda(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name="Usuario Ejecutor")
    codigo_buscado = models.CharField(max_length=50, verbose_name="Código Buscado")
    fecha = models.DateTimeField(auto_now_add=True, verbose_name="Fecha y Hora")

    class Meta:
        verbose_name = "Historial de Búsqueda"
        verbose_name_plural = "Historiales de Búsqueda"
        # Esto asegura que el listado cronológico muestre lo más reciente primero
        ordering = ['-fecha'] 

    def __str__(self):
        return f"{self.usuario.username} buscó {self.codigo_buscado} - {self.fecha.strftime('%d/%m/%Y %H:%M')}"
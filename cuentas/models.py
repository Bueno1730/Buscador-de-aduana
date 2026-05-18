from django.db import models

class Arancel(models.Model):
    # Código arancelario (ej: '0101.21.00.00'). Usamos CharField por los puntos.
    codigo = models.CharField(max_length=20, unique=True, verbose_name="Código")
    descripcion = models.TextField(verbose_name="Descripción de la Mercancía")
    
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
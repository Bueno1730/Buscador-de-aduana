from django.db import models
from cuentas.models import Arancel


class ReferenciaClasificacion(models.Model):
    TIPO_CHOICES = [
        ('resolucion', 'Resolución'),
        ('caso_estudio', 'Caso de Estudio'),
        ('circular', 'Circular'),
        ('normativa', 'Normativa'),
        ('dictamen', 'Dictamen Técnico'),
        ('otro', 'Otro'),
    ]

    ENTIDAD_CHOICES = [
        ('aduana_nacional', 'Aduana Nacional'),
        ('ministerio', 'Ministerio'),
        ('senavexi', 'SENAVEXI'),
        ('ibce', 'IBCE'),
        ('otra', 'Otra'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Título")
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, verbose_name="Tipo de Documento")
    descripcion = models.TextField(verbose_name="Descripción / Contenido")
    archivo = models.FileField(
        upload_to='referencias/archivos/%Y/%m/',
        null=True, blank=True,
        verbose_name="Archivo (PDF)"
    )
    enlace = models.URLField(max_length=500, null=True, blank=True, verbose_name="Enlace externo")
    codigos_arancelarios = models.ManyToManyField(
        Arancel,
        blank=True,
        verbose_name="Códigos Arancelarios Relacionados"
    )
    entidad_emisora = models.CharField(
        max_length=50, choices=ENTIDAD_CHOICES,
        verbose_name="Entidad Emisora"
    )
    fecha_emision = models.DateField(verbose_name="Fecha de Emisión")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Registro")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    class Meta:
        verbose_name = "Referencia de Clasificación"
        verbose_name_plural = "Referencias de Clasificación"
        ordering = ['-fecha_emision']

    def __str__(self):
        return f"{self.get_tipo_display()}: {self.titulo[:60]}"

from django import forms
from django.core.exceptions import ValidationError
from .models import ReporteError
import re

MAX_IMAGE_SIZE = 5 * 1024 * 1024

class ReporteErrorForm(forms.ModelForm):
    class Meta:
        model = ReporteError
        fields = [
            'titulo', 'categoria', 'descripcion',
            'partida_arancelaria_afectada', 'codigo_producto_afectado',
            'captura_pantalla', 'nombre_reportante', 'email_reportante'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Error en tarifa de partida 8471.30.01'}),
            'categoria': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Describe el error con detalle...'}),
            'partida_arancelaria_afectada': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: 8471.30.01'}),
            'codigo_producto_afectado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: PROD-2024-001'}),
            'nombre_reportante': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'email_reportante': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'tu@email.com'}),
            'captura_pantalla': forms.FileInput(attrs={'accept': '.jpg, .jpeg, .png'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.errors:
            for field_name in self.errors:
                if field_name in self.fields:
                    widget = self.fields[field_name].widget
                    existing = widget.attrs.get('class', '')
                    if 'is-invalid' not in existing:
                        widget.attrs['class'] = f'{existing} is-invalid'.strip()

    def clean_nombre_reportante(self):
        nombre = self.cleaned_data.get('nombre_reportante', '')
        if not re.match(r'^[a-zA-ZáéíóúÁÉÍÓÚñÑüÜ\s]+$', nombre):
            raise ValidationError('El nombre solo puede contener letras.')
        return nombre

    def clean_email_reportante(self):
        email = self.cleaned_data.get('email_reportante', '')
        if ' ' in email:
            raise ValidationError('El correo no puede contener espacios.')
        if not re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email):
            raise ValidationError('Por favor, introduce un correo electrónico válido.')
        return email

    def clean_partida_arancelaria_afectada(self):
        partida = self.cleaned_data.get('partida_arancelaria_afectada', '')
        if partida:
            if ' ' in partida:
                raise ValidationError('La partida arancelaria no puede contener espacios.')
            if not re.match(r'^[0-9.]+$', partida):
                raise ValidationError('La partida arancelaria solo puede contener números.')
        return partida

    def clean_codigo_producto_afectado(self):
        codigo = self.cleaned_data.get('codigo_producto_afectado', '')
        if codigo and ' ' in codigo:
            raise ValidationError('El código de producto no puede contener espacios.')
        return codigo

    def clean_captura_pantalla(self):
        imagen = self.cleaned_data.get('captura_pantalla')
        if imagen:
            if imagen.size > MAX_IMAGE_SIZE:
                raise ValidationError(f'La imagen no debe superar los 5 MB. El archivo actual pesa {imagen.size / (1024*1024):.1f} MB.')
        return imagen
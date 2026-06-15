from django import forms
from .models import ReferenciaClasificacion


class BusquedaReferenciaForm(forms.Form):
    texto = forms.CharField(
        required=False,
        label="Buscar",
        widget=forms.TextInput(attrs={
            'placeholder': 'Buscar por título, descripción...',
            'class': 'input-texto'
        })
    )
    tipo = forms.ChoiceField(
        required=False,
        label="Tipo",
        choices=[('', 'Todos los tipos')] + ReferenciaClasificacion.TIPO_CHOICES
    )
    codigo_arancelario = forms.CharField(
        required=False,
        label="Código Arancelario",
        widget=forms.TextInput(attrs={
            'placeholder': 'Ej: 0101.21',
            'class': 'input-codigo'
        })
    )

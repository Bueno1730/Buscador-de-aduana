from django import forms
from .models import ReporteError

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
        }
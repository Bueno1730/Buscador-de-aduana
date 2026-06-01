from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Arancel

class ArancelForm(forms.ModelForm):
    class Meta:
        model = Arancel
        fields = '__all__' # <-- Llama a todos los campos del nuevo modelo

    def __init__(self, *args, **kwargs):
        super(ArancelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'
            })
        
        # Hacemos que la caja de descripción sea más pequeña
        self.fields['descripcion'].widget.attrs.update({'rows': '3'})

    # TRASLADO DE TU HISTORIA DE USUARIO: Validaciones del código
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        # Criterio 2: Validación de formato (solo números y puntos)
        if not re.match(r'^[0-9.]+$', codigo):
            raise ValidationError("El código debe contener únicamente números y puntos (Ej: 01.05.11.00.00).")

        # Criterio 3: Prevención de duplicados
        if Arancel.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este código arancelario ya se encuentra registrado en el sistema.")

        return codigo
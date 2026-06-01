from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Arancel
from django.contrib.auth.forms import AuthenticationForm

class ArancelForm(forms.ModelForm):
    class Meta:
        model = Arancel
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ArancelForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'
            })
        
        self.fields['descripcion'].widget.attrs.update({'rows': '3'})

    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo')

        if not re.match(r'^[0-9.]+$', codigo):
            raise ValidationError("El código debe contener únicamente números y puntos (Ej: 01.05.11.00.00).")

        if Arancel.objects.filter(codigo=codigo).exclude(pk=self.instance.pk).exists():
            raise ValidationError("Este código arancelario ya se encuentra registrado en el sistema.")

        return codigo

class CustomLoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Credenciales incorrectas. Verifique su usuario y contraseña.",
        'inactive': "Esta cuenta está inactiva.",
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'
            })
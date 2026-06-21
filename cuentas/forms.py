from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Arancel
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User  # <-- Importación añadida para la gestión de personal

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


# ==========================================
# NUEVO FORMULARIO: GESTIÓN DE PERSONAL
# ==========================================
class UsuarioPersonalForm(forms.ModelForm):
    ROL_CHOICES = (
        ('despachante', 'Despachante de Aduana'),
        ('administrador', 'Administrador del Sistema'),
    )
    
    rol = forms.ChoiceField(
        choices=ROL_CHOICES, 
        label="Rol del Usuario", 
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'
        }), 
        required=False, 
        label="Contraseña",
        help_text="Déjalo en blanco si estás editando y no quieres cambiarla."
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'}),
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 mb-2'}),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Asignación estricta de roles según el formulario
        if self.cleaned_data['rol'] == 'administrador':
            user.is_staff = True
            user.is_superuser = True 
        else:
            user.is_staff = False
            user.is_superuser = False

        # Encriptar la contraseña si se escribió una nueva
        if self.cleaned_data['password']:
            user.set_password(self.cleaned_data['password'])

        if commit:
            user.save()
        return user
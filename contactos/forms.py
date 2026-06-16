import re
from django import forms
from .models import Contacto


def _validar_telefono(telefono):
    if telefono:
        limpio = re.sub(r'[\s\-\(\)]', '', telefono)
        if not re.match(r'^\+?\d{6,15}$', limpio):
            raise forms.ValidationError(
                'Introduce un número de teléfono válido '
                '(solo números, entre 6 y 15 dígitos).'
            )
    return telefono


class ContactoMayorForm(forms.ModelForm):
    """Formulario simplificado para el mayor."""
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'categoria']
        labels = {
            'nombre': '¿Cómo se llama?',
            'telefono': 'Teléfono',
            'categoria': 'Tipo de contacto',
        }

    def clean_telefono(self):
        return _validar_telefono(self.cleaned_data.get('telefono', ''))


class ContactoEditorForm(forms.ModelForm):
    """Formulario completo para el familiar-editor."""
    class Meta:
        model = Contacto
        fields = ['nombre', 'telefono', 'categoria', 'direccion', 'notas']
        labels = {
            'nombre': 'Nombre',
            'telefono': 'Teléfono',
            'categoria': 'Categoría',
            'direccion': 'Dirección',
            'notas': 'Notas',
        }
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 2}),
            'notas': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_telefono(self):
        return _validar_telefono(self.cleaned_data.get('telefono', ''))

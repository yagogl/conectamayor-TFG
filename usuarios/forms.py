from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario


class RegistroForm(UserCreationForm):
    ROL_CHOICES = [
        ('mayor', 'Soy la persona mayor'),
        ('editor', 'Soy familiar de confianza (puedo gestionar todo)'),
        ('amigo', 'Soy familiar o amigo'),
    ]

    rol = forms.ChoiceField(
        choices=ROL_CHOICES,
        widget=forms.RadioSelect,
        label='¿Quién eres?'
    )
    nombre_grupo = forms.CharField(
        max_length=100,
        required=False,
        label='Nombre del grupo familiar (opcional)',
        help_text='Solo si eres el familiar de confianza que crea el grupo.'
    )
    codigo_grupo = forms.CharField(
        max_length=10,
        required=False,
        label='Código del grupo familiar',
        help_text=(
            'Si ya te han dado un código (ej: FAM-7X2K), '
            'escríbelo aquí para unirte.'
        )
    )
    first_name = forms.CharField(max_length=50, label='Nombre')
    last_name = forms.CharField(
        max_length=50, label='Apellidos', required=False
    )
    telefono = forms.CharField(
        max_length=20,
        required=False,
        label='Tu número de teléfono (opcional)',
        help_text='Para que tu familia pueda llamarte desde la app.'
    )

    class Meta:
        model = Usuario
        fields = [
            'username', 'first_name', 'last_name',
            'telefono', 'password1', 'password2',
        ]
        labels = {
            'username': (
                'Nombre de usuario (este nombre usarás para entrar en la app)'
            ),
        }
        help_texts = {
            'username': (
                'Elige un nombre fácil de recordar. '
                'Por ejemplo: maria, abuela, pepe.'
            ),
        }

    def clean_username(self):
        username = self.cleaned_data['username']
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError(
                f'El nombre "{username}" ya está en uso. '
                f'Prueba con: {username}1, {username}2 o añade tu apellido.'
            )
        return username


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['first_name', 'last_name', 'telefono', 'foto_perfil']
        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'telefono': 'Teléfono',
            'foto_perfil': 'Foto de perfil',
        }

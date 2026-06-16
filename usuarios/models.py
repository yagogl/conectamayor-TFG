from django.contrib.auth.models import AbstractUser
from django.db import models
import random
import string


def generar_codigo():
    """Genera un código único de 6 caracteres tipo FAM-7X2K"""
    chars = string.ascii_uppercase + string.digits
    return 'FAM-' + ''.join(random.choices(chars, k=4))


class GrupoFamiliar(models.Model):
    codigo = models.CharField(max_length=10, unique=True, default=generar_codigo)
    nombre = models.CharField(max_length=100, blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Grupo {self.codigo} — {self.nombre}"


class Usuario(AbstractUser):
    ROL_CHOICES = [
        ('mayor', 'Persona Mayor'),
        ('editor', 'Familiar Editor'),
        ('amigo', 'Familiar / Amigo'),
    ]

    rol = models.CharField(max_length=10, choices=ROL_CHOICES, default='amigo')
    telefono = models.CharField(max_length=20, blank=True, verbose_name='Teléfono')
    grupo_familiar = models.ForeignKey(
        GrupoFamiliar,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='miembros'
    )
    foto_perfil = models.ImageField(upload_to='perfiles/', null=True, blank=True)

    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_rol_display()})"

    @property
    def es_mayor(self):
        return self.rol == 'mayor'

    @property
    def es_editor(self):
        return self.rol == 'editor'

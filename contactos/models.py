from django.db import models
from usuarios.models import Usuario


class Contacto(models.Model):
    CATEGORIA_CHOICES = [
        ('familia', 'Familia'),
        ('medico', 'Médico'),
        ('farmacia', 'Farmacia'),
        ('vecino', 'Vecino'),
        ('otro', 'Otro'),
    ]

    usuario_mayor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='contactos'
    )
    nombre = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True)
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default='otro')
    direccion = models.TextField(blank=True)
    notas = models.TextField(blank=True)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['categoria', 'nombre']

    def __str__(self):
        return f"{self.nombre} ({self.get_categoria_display()})"

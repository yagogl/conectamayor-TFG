from django.db import models
from usuarios.models import Usuario


class Recordatorio(models.Model):
    TIPO_CHOICES = [
        ('pastilla', 'Pastilla'),
        ('medico', 'Médico'),
        ('llamada', 'Llamada'),
        ('cumple', 'Cumpleaños'),
        ('otro', 'Otro'),
    ]

    usuario_mayor = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='recordatorios'
    )
    titulo = models.CharField(max_length=200)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES, default='otro')
    fecha = models.DateField()
    hora = models.TimeField(null=True, blank=True)
    hecho = models.BooleanField(default=False)
    creado_por = models.ForeignKey(
        Usuario,
        on_delete=models.SET_NULL,
        null=True,
        related_name='recordatorios_creados'
    )
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['fecha', 'hora']

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"

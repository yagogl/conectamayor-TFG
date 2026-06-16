from django.db import models
from usuarios.models import Usuario


class Mensaje(models.Model):
    remitente = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes_enviados'
    )
    destinatario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='mensajes_recibidos'
    )
    texto = models.TextField()
    enviado_en = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)

    class Meta:
        ordering = ['enviado_en']

    def __str__(self):
        return f"{self.remitente} → {self.destinatario}: {self.texto[:40]}"

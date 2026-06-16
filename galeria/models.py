from django.db import models
from usuarios.models import Usuario


class Foto(models.Model):
    grupo_familiar = models.ForeignKey(
        'usuarios.GrupoFamiliar',
        on_delete=models.CASCADE,
        related_name='fotos'
    )
    subida_por = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='fotos_subidas'
    )
    imagen = models.ImageField(upload_to='galeria/')
    titulo = models.CharField(max_length=200, blank=True)
    subida_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-subida_en']

    def __str__(self):
        return self.titulo or f"Foto de {self.subida_por} ({self.subida_en.date()})"


class Comentario(models.Model):
    foto = models.ForeignKey(Foto, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    texto = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['creado_en']

    def __str__(self):
        return f"{self.autor}: {self.texto[:40]}"

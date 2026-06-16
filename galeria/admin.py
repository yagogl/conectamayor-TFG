from django.contrib import admin
from .models import Foto, Comentario

@admin.register(Foto)
class FotoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'subida_por', 'grupo_familiar', 'subida_en']

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ['autor', 'foto', 'creado_en']

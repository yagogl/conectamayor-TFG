from django.contrib import admin
from .models import Recordatorio

@admin.register(Recordatorio)
class RecordatorioAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'fecha', 'hora', 'hecho', 'usuario_mayor']
    list_filter = ['tipo', 'hecho']

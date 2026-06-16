from django.contrib import admin
from .models import Contacto

@admin.register(Contacto)
class ContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'categoria', 'telefono', 'usuario_mayor']
    list_filter = ['categoria']

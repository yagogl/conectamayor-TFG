from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, GrupoFamiliar


@admin.register(GrupoFamiliar)
class GrupoFamiliarAdmin(admin.ModelAdmin):
    list_display = ['codigo', 'nombre', 'creado_en']
    readonly_fields = ['codigo', 'creado_en']


@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    list_display = ['username', 'get_full_name', 'rol', 'grupo_familiar', 'telefono']
    list_filter = ['rol']
    fieldsets = UserAdmin.fieldsets + (
        ('ConectaMayor', {'fields': ('rol', 'grupo_familiar', 'telefono', 'foto_perfil')}),
    )

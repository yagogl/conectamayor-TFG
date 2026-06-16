from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Usuario, GrupoFamiliar
from .forms import RegistroForm, PerfilForm
from agenda.models import Recordatorio
from mensajes.models import Mensaje
from galeria.models import Foto


def inicio(request):
    """Redirige al login o a la pantalla correcta según el rol."""
    if not request.user.is_authenticated:
        return redirect('login')
    if request.user.es_mayor:
        return redirect('inicio_mayor')
    return redirect('inicio_familiar')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'usuarios/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            rol = form.cleaned_data['rol']
            user.rol = rol

            if rol == 'editor':
                nombre_grupo = form.cleaned_data.get('nombre_grupo', '')
                grupo = GrupoFamiliar.objects.create(nombre=nombre_grupo)
                user.grupo_familiar = grupo
            else:
                codigo = form.cleaned_data.get(
                    'codigo_grupo', ''
                ).strip().upper()
                if codigo:
                    try:
                        grupo = GrupoFamiliar.objects.get(codigo=codigo)
                        user.grupo_familiar = grupo
                    except GrupoFamiliar.DoesNotExist:
                        messages.error(
                            request,
                            f'El código "{codigo}" no existe. '
                            f'Puedes unirte más tarde.'
                        )

            user.save()
            login(request, user)

            if rol == 'editor':
                messages.success(
                    request,
                    f'Grupo familiar creado. '
                    f'Tu código es: {user.grupo_familiar.codigo}'
                )
            elif user.grupo_familiar:
                messages.success(
                    request,
                    'Te has unido al grupo '
                    f'{user.grupo_familiar.nombre or user.grupo_familiar.codigo}'
                    '.'
                )
            else:
                messages.info(
                    request,
                    'Cuenta creada. Únete a un grupo familiar '
                    'con el código que te han compartido.'
                )
            return redirect('inicio')
    else:
        form = RegistroForm()
    return render(request, 'usuarios/registro.html', {'form': form})


@login_required
def unirse_grupo(request):
    """Permite a un usuario sin grupo unirse con un código."""
    if request.user.grupo_familiar:
        messages.info(request, 'Ya perteneces a un grupo familiar.')
        return redirect('inicio')

    if request.method == 'POST':
        codigo = request.POST.get('codigo', '').strip().upper()
        try:
            grupo = GrupoFamiliar.objects.get(codigo=codigo)
            request.user.grupo_familiar = grupo
            request.user.save()
            messages.success(
                request,
                f'Te has unido al grupo {grupo.nombre or codigo}.'
            )
            return redirect('inicio')
        except GrupoFamiliar.DoesNotExist:
            messages.error(
                request,
                'Código incorrecto. Comprueba que lo has escrito bien.'
            )

    return render(request, 'usuarios/unirse_grupo.html')


@login_required
def inicio_mayor(request):
    if not request.user.es_mayor:
        return redirect('inicio_familiar')

    hoy = timezone.localdate()
    recordatorios_hoy_lista = Recordatorio.objects.filter(
        usuario_mayor=request.user,
        fecha=hoy,
        hecho=False
    )

    mensajes_nuevos = Mensaje.objects.filter(
        destinatario=request.user,
        leido=False
    ).count()

    fotos_nuevas = 0
    if request.user.grupo_familiar:
        hace_24h = timezone.now() - timedelta(hours=24)
        fotos_nuevas = Foto.objects.filter(
            grupo_familiar=request.user.grupo_familiar,
            subida_en__gte=hace_24h
        ).count()

    return render(request, 'usuarios/mayor/inicio.html', {
        'recordatorios_hoy': recordatorios_hoy_lista.count(),
        'recordatorios_hoy_lista': recordatorios_hoy_lista,
        'mensajes_nuevos': mensajes_nuevos,
        'fotos_nuevas': fotos_nuevas,
    })


@login_required
def inicio_familiar(request):
    if request.user.es_mayor:
        return redirect('inicio_mayor')

    mayores = []
    if request.user.grupo_familiar:
        mayores = Usuario.objects.filter(
            grupo_familiar=request.user.grupo_familiar,
            rol='mayor'
        )

    return render(request, 'usuarios/familiar/inicio.html', {
        'mayores': mayores,
    })


@login_required
def perfil(request):
    if request.method == 'POST':
        form = PerfilForm(
            request.POST, request.FILES, instance=request.user
        )
        if form.is_valid():
            form.save()
            messages.success(request, '¡Perfil actualizado!')
            return redirect('perfil')
    else:
        form = PerfilForm(instance=request.user)
    return render(request, 'usuarios/perfil.html', {'form': form})

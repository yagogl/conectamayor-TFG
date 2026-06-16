from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import Recordatorio
from .forms import RecordatorioMayorForm, RecordatorioEditorForm
from usuarios.models import Usuario


@login_required
def lista(request):
    """Vista principal de agenda — muestra hoy + 6 días."""
    user = request.user

    if user.es_mayor:
        mayor = user
    elif user.grupo_familiar:
        mayor_id = request.GET.get('mayor')
        if mayor_id:
            mayor = Usuario.objects.filter(
                pk=mayor_id,
                grupo_familiar=user.grupo_familiar,
                rol='mayor'
            ).first()
        else:
            mayor = Usuario.objects.filter(
                grupo_familiar=user.grupo_familiar,
                rol='mayor'
            ).first()
    else:
        mayor = None

    mayores = []
    if not user.es_mayor and user.grupo_familiar:
        mayores = Usuario.objects.filter(
            grupo_familiar=user.grupo_familiar,
            rol='mayor'
        )

    hoy = timezone.localdate()
    dias = []
    for i in range(7):
        dia = hoy + timedelta(days=i)
        recordatorios_dia = []
        if mayor:
            recordatorios_dia = Recordatorio.objects.filter(
                usuario_mayor=mayor,
                fecha=dia
            )
        dias.append({
            'fecha': dia,
            'es_hoy': i == 0,
            'recordatorios': recordatorios_dia,
        })

    return render(request, 'agenda/lista.html', {
        'dias': dias,
        'mayor': mayor,
        'mayores': mayores,
        'hoy': hoy,
    })


@login_required
def nuevo_recordatorio(request):
    """Formulario adaptado según el rol."""
    user = request.user

    if user.es_mayor:
        mayor = user
        FormClass = RecordatorioMayorForm
        template = 'agenda/mayor/nuevo.html'
    elif user.es_editor and user.grupo_familiar:
        mayor_id = request.GET.get('mayor')
        if mayor_id:
            mayor = Usuario.objects.filter(
                pk=mayor_id,
                grupo_familiar=user.grupo_familiar,
                rol='mayor'
            ).first()
        else:
            mayor = Usuario.objects.filter(
                grupo_familiar=user.grupo_familiar,
                rol='mayor'
            ).first()
        if not mayor:
            messages.error(request, 'No hay ninguna persona mayor en tu grupo todavía.')
            return redirect('agenda:lista')
        FormClass = RecordatorioEditorForm
        template = 'agenda/familiar/nuevo.html'
    else:
        messages.error(request, 'No tienes permisos para añadir recordatorios.')
        return redirect('agenda:lista')

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            recordatorio = form.save(commit=False)
            recordatorio.usuario_mayor = mayor
            recordatorio.creado_por = user
            recordatorio.save()
            messages.success(request, '¡Recordatorio guardado!')
            return redirect('agenda:lista')
    else:
        form = FormClass()

    return render(request, template, {'form': form, 'mayor': mayor})


@login_required
def marcar_hecho(request, pk):
    recordatorio = get_object_or_404(Recordatorio, pk=pk)
    recordatorio.hecho = not recordatorio.hecho
    recordatorio.save()
    return redirect('agenda:lista')


@login_required
def recordar_mas_tarde(request, pk):
    """Mueve el recordatorio al día siguiente."""
    recordatorio = get_object_or_404(Recordatorio, pk=pk)
    recordatorio.fecha = recordatorio.fecha + timedelta(days=1)
    recordatorio.hecho = False
    recordatorio.save()
    messages.info(request, 'Recordatorio movido a mañana.')
    return redirect('agenda:lista')


@login_required
def editar_recordatorio(request, pk):
    recordatorio = get_object_or_404(Recordatorio, pk=pk)
    user = request.user

    if user.es_mayor:
        FormClass = RecordatorioMayorForm
        template = 'agenda/mayor/nuevo.html'
    else:
        FormClass = RecordatorioEditorForm
        template = 'agenda/familiar/nuevo.html'

    if request.method == 'POST':
        form = FormClass(request.POST, instance=recordatorio)
        if form.is_valid():
            form.save()
            messages.success(request, 'Recordatorio actualizado.')
            return redirect('agenda:lista')
    else:
        form = FormClass(instance=recordatorio)

    return render(request, template, {'form': form, 'editar': True})


@login_required
def borrar_recordatorio(request, pk):
    recordatorio = get_object_or_404(Recordatorio, pk=pk)
    if request.user.es_editor or request.user.es_mayor:
        recordatorio.delete()
        messages.success(request, 'Recordatorio eliminado.')
    return redirect('agenda:lista')

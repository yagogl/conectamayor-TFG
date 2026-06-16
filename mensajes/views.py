from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils import timezone
from .models import Mensaje
from usuarios.models import Usuario


@login_required
def lista(request):
    """Muestra las conversaciones del usuario."""
    user = request.user
    if not user.grupo_familiar:
        return render(request, 'mensajes/lista.html', {'conversaciones': []})

    # Obtener todos los miembros del grupo menos yo
    miembros = Usuario.objects.filter(
        grupo_familiar=user.grupo_familiar
    ).exclude(pk=user.pk)

    # Para cada miembro, obtener el último mensaje
    conversaciones = []
    for miembro in miembros:
        ultimo = Mensaje.objects.filter(
            remitente__in=[user, miembro],
            destinatario__in=[user, miembro]
        ).order_by('-enviado_en').first()

        no_leidos = Mensaje.objects.filter(
            remitente=miembro,
            destinatario=user,
            leido=False
        ).count()

        conversaciones.append({
            'miembro': miembro,
            'ultimo': ultimo,
            'no_leidos': no_leidos,
        })

    return render(request, 'mensajes/lista.html', {
        'conversaciones': conversaciones,
    })


@login_required
def conversacion(request, usuario_id):
    """Chat 1 a 1 con un usuario."""
    user = request.user
    otro = get_object_or_404(Usuario, pk=usuario_id)

    # Marcar como leídos los mensajes recibidos
    Mensaje.objects.filter(
        remitente=otro,
        destinatario=user,
        leido=False
    ).update(leido=True)

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        if texto:
            Mensaje.objects.create(
                remitente=user,
                destinatario=otro,
                texto=texto
            )
        return redirect('mensajes:conversacion', usuario_id=usuario_id)

    mensajes = Mensaje.objects.filter(
        remitente__in=[user, otro],
        destinatario__in=[user, otro]
    ).order_by('enviado_en')

    return render(request, 'mensajes/conversacion.html', {
        'otro': otro,
        'mensajes': mensajes,
    })


@login_required
def mensajes_nuevos(request, usuario_id):
    """Endpoint AJAX — devuelve mensajes nuevos desde un ID dado."""
    user = request.user
    otro = get_object_or_404(Usuario, pk=usuario_id)
    desde_id = int(request.GET.get('desde', 0))

    mensajes = Mensaje.objects.filter(
        remitente__in=[user, otro],
        destinatario__in=[user, otro],
        pk__gt=desde_id
    ).order_by('enviado_en')

    # Marcar como leídos
    mensajes.filter(destinatario=user).update(leido=True)

    datos = [{
        'id': m.pk,
        'texto': m.texto,
        'propio': m.remitente == user,
        'hora': m.enviado_en.strftime('%H:%M'),
        'nombre': m.remitente.first_name or m.remitente.username,
    } for m in mensajes]

    return JsonResponse({'mensajes': datos})

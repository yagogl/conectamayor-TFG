from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Foto, Comentario
from usuarios.models import Usuario


@login_required
def lista(request):
    user = request.user
    if not user.grupo_familiar:
        return render(request, 'galeria/lista.html', {'fotos': []})

    fotos = Foto.objects.filter(
        grupo_familiar=user.grupo_familiar
    ).order_by('-subida_en')

    return render(request, 'galeria/lista.html', {'fotos': fotos})


@login_required
def subir_foto(request):
    if not request.user.grupo_familiar:
        messages.error(request, 'Únete a un grupo familiar primero.')
        return redirect('galeria:lista')

    if request.method == 'POST':
        imagen = request.FILES.get('imagen')
        titulo = request.POST.get('titulo', '').strip()
        if imagen:
            Foto.objects.create(
                grupo_familiar=request.user.grupo_familiar,
                subida_por=request.user,
                imagen=imagen,
                titulo=titulo
            )
            messages.success(request, '¡Foto subida!')
            return redirect('galeria:lista')
        else:
            messages.error(request, 'Selecciona una imagen.')

    return render(request, 'galeria/subir.html')


@login_required
def detalle_foto(request, pk):
    foto = get_object_or_404(Foto, pk=pk)

    if request.method == 'POST':
        texto = request.POST.get('texto', '').strip()
        if texto:
            Comentario.objects.create(
                foto=foto,
                autor=request.user,
                texto=texto
            )
        return redirect('galeria:detalle', pk=pk)

    comentarios = foto.comentarios.all()
    return render(request, 'galeria/detalle.html', {
        'foto': foto,
        'comentarios': comentarios,
    })


@login_required
def borrar_foto(request, pk):
    foto = get_object_or_404(Foto, pk=pk)
    if request.user == foto.subida_por or request.user.es_editor:
        foto.delete()
        messages.success(request, 'Foto eliminada.')
    return redirect('galeria:lista')

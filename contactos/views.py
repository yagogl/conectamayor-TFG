from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Contacto
from .forms import ContactoMayorForm, ContactoEditorForm
from usuarios.models import Usuario


@login_required
def lista(request):
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

    contactos = []
    if mayor:
        contactos = Contacto.objects.filter(usuario_mayor=mayor)

    categorias = {}
    for c in contactos:
        cat = c.get_categoria_display()
        if cat not in categorias:
            categorias[cat] = []
        categorias[cat].append(c)

    miembros = []
    if user.grupo_familiar:
        miembros = Usuario.objects.filter(
            grupo_familiar=user.grupo_familiar
        ).exclude(pk=user.pk).order_by('first_name')

    return render(request, 'contactos/lista.html', {
        'categorias': categorias,
        'mayor': mayor,
        'mayores': mayores,
        'miembros': miembros,
    })


@login_required
def nuevo_contacto(request):
    user = request.user

    if user.es_mayor:
        mayor = user
        FormClass = ContactoMayorForm
        template = 'contactos/mayor/nuevo.html'
    elif user.es_editor and user.grupo_familiar:
        mayor = Usuario.objects.filter(
            grupo_familiar=user.grupo_familiar,
            rol='mayor'
        ).first()
        if not mayor:
            messages.error(
                request,
                'No hay ninguna persona mayor en tu grupo todavía.'
            )
            return redirect('contactos:lista')
        FormClass = ContactoEditorForm
        template = 'contactos/familiar/nuevo.html'
    else:
        messages.error(request, 'No tienes permisos para añadir contactos.')
        return redirect('contactos:lista')

    if request.method == 'POST':
        form = FormClass(request.POST)
        if form.is_valid():
            contacto = form.save(commit=False)
            contacto.usuario_mayor = mayor
            contacto.save()
            messages.success(request, '¡Contacto guardado!')
            return redirect('contactos:lista')
    else:
        form = FormClass()

    return render(request, template, {'form': form, 'mayor': mayor})


@login_required
def editar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    user = request.user

    if user.es_mayor:
        FormClass = ContactoMayorForm
        template = 'contactos/mayor/nuevo.html'
    else:
        FormClass = ContactoEditorForm
        template = 'contactos/familiar/nuevo.html'

    if request.method == 'POST':
        form = FormClass(request.POST, instance=contacto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Contacto actualizado.')
            return redirect('contactos:lista')
    else:
        form = FormClass(instance=contacto)

    return render(request, template, {'form': form, 'editar': True})


@login_required
def borrar_contacto(request, pk):
    contacto = get_object_or_404(Contacto, pk=pk)
    if request.user.es_editor or request.user.es_mayor:
        contacto.delete()
        messages.success(request, 'Contacto eliminado.')
    return redirect('contactos:lista')

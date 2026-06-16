"""
seed_demo.py — Datos de demostración para la aplicación ConectaMayor.

Crea un grupo familiar de ejemplo (Familia González-Pérez) con dos
personas mayores, un familiar editor y un familiar de solo lectura,
junto con recordatorios, contactos y mensajes de muestra.

Uso:
    python manage.py shell < seed_demo.py

Nota: las fotografías de la galería deben subirse manualmente desde la
aplicación, ya que requieren archivos de imagen reales.
"""

from datetime import timedelta
from django.utils import timezone
from django.contrib.auth import get_user_model

from usuarios.models import GrupoFamiliar
from agenda.models import Recordatorio
from contactos.models import Contacto
from mensajes.models import Mensaje


Usuario = get_user_model()
now = timezone.now()
hoy = now.date()


# ----------------------------------------------------------------------------
# 1. GRUPO FAMILIAR
# ----------------------------------------------------------------------------

grupo, _ = GrupoFamiliar.objects.get_or_create(
    codigo="FAM-A3K9",
    defaults={"nombre": "Familia González-Pérez"},
)
print(f"OK - Grupo familiar: {grupo.codigo}")


# ----------------------------------------------------------------------------
# 2. USUARIOS
# ----------------------------------------------------------------------------

usuarios_datos = [
    {
        "username": "carmen",
        "password": "Carmen2026",
        "first_name": "Carmen",
        "last_name": "Pérez Ruiz",
        "email": "carmen.perez@ejemplo.es",
        "rol": "mayor",
    },
    {
        "username": "antonio",
        "password": "Antonio2026",
        "first_name": "Antonio",
        "last_name": "González Martín",
        "email": "antonio.gonzalez@ejemplo.es",
        "rol": "mayor",
    },
    {
        "username": "laura",
        "password": "Laura2026",
        "first_name": "Laura",
        "last_name": "González Pérez",
        "email": "laura.gonzalez@ejemplo.es",
        "rol": "editor",
    },
    {
        "username": "miguel",
        "password": "Miguel2026",
        "first_name": "Miguel",
        "last_name": "González Pérez",
        "email": "miguel.gonzalez@ejemplo.es",
        "rol": "amigo",
    },
]

usuarios = {}
for datos in usuarios_datos:
    user, creado = Usuario.objects.get_or_create(
        username=datos["username"],
        defaults={
            "first_name": datos["first_name"],
            "last_name": datos["last_name"],
            "email": datos["email"],
            "rol": datos["rol"],
            "grupo_familiar": grupo,
        },
    )
    user.set_password(datos["password"])
    user.grupo_familiar = grupo
    user.rol = datos["rol"]
    user.save()
    usuarios[datos["username"]] = user
    print(f"OK - Usuario: {user.username} ({user.rol})")

carmen = usuarios["carmen"]
antonio = usuarios["antonio"]
laura = usuarios["laura"]
miguel = usuarios["miguel"]


# ----------------------------------------------------------------------------
# 3. RECORDATORIOS
#    Tipos válidos: pastilla, medico, llamada, cumple, otro
# ----------------------------------------------------------------------------

Recordatorio.objects.filter(usuario_mayor__in=[carmen, antonio]).delete()

recordatorios_carmen = [
    # HOY (generan badge de notificación en la pantalla principal)
    {"titulo": "Tomar la pastilla de la tensión",
     "fecha": hoy, "hora": "09:00", "tipo": "pastilla"},
    {"titulo": "Llamar al fisioterapeuta",
     "fecha": hoy, "hora": "11:30", "tipo": "llamada"},

    # Próximos días
    {"titulo": "Cita con el cardiólogo",
     "fecha": hoy + timedelta(days=2), "hora": "10:15", "tipo": "medico"},
    {"titulo": "Cumpleaños de Sofía",
     "fecha": hoy + timedelta(days=3), "hora": "14:00", "tipo": "cumple"},
    {"titulo": "Tomar la pastilla de la tensión",
     "fecha": hoy + timedelta(days=1), "hora": "09:00", "tipo": "pastilla"},
    {"titulo": "Análisis de sangre en ayunas",
     "fecha": hoy + timedelta(days=5), "hora": "08:30", "tipo": "medico"},
]

recordatorios_antonio = [
    # HOY
    {"titulo": "Tomar la pastilla del azúcar",
     "fecha": hoy, "hora": "08:00", "tipo": "pastilla"},
    {"titulo": "Paseo por el parque",
     "fecha": hoy, "hora": "18:00", "tipo": "otro"},

    # Próximos días
    {"titulo": "Revisión del oculista",
     "fecha": hoy + timedelta(days=1), "hora": "12:00", "tipo": "medico"},
    {"titulo": "Tomar la pastilla del azúcar",
     "fecha": hoy + timedelta(days=1), "hora": "08:00", "tipo": "pastilla"},
    {"titulo": "Cumpleaños de Miguel",
     "fecha": hoy + timedelta(days=4), "hora": "20:00", "tipo": "cumple"},
    {"titulo": "Cita con el podólogo",
     "fecha": hoy + timedelta(days=6), "hora": "17:30", "tipo": "medico"},
]


def crear_recordatorios(mayor, lista):
    for r in lista:
        Recordatorio.objects.create(
            usuario_mayor=mayor,
            creado_por=laura,
            titulo=r["titulo"],
            fecha=r["fecha"],
            hora=r["hora"],
            tipo=r["tipo"],
            hecho=False,
        )


crear_recordatorios(carmen, recordatorios_carmen)
crear_recordatorios(antonio, recordatorios_antonio)
print(f"OK - Recordatorios: {len(recordatorios_carmen)} para Carmen, "
      f"{len(recordatorios_antonio)} para Antonio")


# ----------------------------------------------------------------------------
# 4. CONTACTOS
#    Categorías válidas: familia, medico, farmacia, vecino, otro
# ----------------------------------------------------------------------------

Contacto.objects.filter(usuario_mayor__in=[carmen, antonio]).delete()

contactos_carmen = [
    # Familia
    {"nombre": "Laura (hija)", "telefono": "612 345 678",
     "categoria": "familia", "notas": "Disponible por las tardes"},
    {"nombre": "Miguel (hijo)", "telefono": "612 987 654",
     "categoria": "familia", "notas": ""},
    {"nombre": "Sofía (nieta)", "telefono": "611 222 333",
     "categoria": "familia", "notas": ""},
    # Médico
    {"nombre": "Dr. Hernández (cardiólogo)", "telefono": "915 123 456",
     "categoria": "medico", "notas": "Hospital La Paz, planta 3"},
    {"nombre": "Centro de salud", "telefono": "915 789 012",
     "categoria": "medico", "notas": "Cita previa por teléfono"},
    # Farmacia
    {"nombre": "Farmacia del barrio", "telefono": "915 444 555",
     "categoria": "farmacia", "notas": "Reparto a domicilio"},
    # Vecino
    {"nombre": "Pilar (vecina del 2ºB)", "telefono": "611 333 444",
     "categoria": "vecino", "notas": "Por si hay alguna urgencia"},
    # Otro
    {"nombre": "Taxi", "telefono": "915 555 666",
     "categoria": "otro", "notas": ""},
]

contactos_antonio = [
    # Familia
    {"nombre": "Laura (hija)", "telefono": "612 345 678",
     "categoria": "familia", "notas": ""},
    {"nombre": "Miguel (hijo)", "telefono": "612 987 654",
     "categoria": "familia", "notas": ""},
    {"nombre": "Carlos (hermano)", "telefono": "918 111 222",
     "categoria": "familia", "notas": "Vive en Valencia"},
    # Médico
    {"nombre": "Dra. Ramírez (endocrina)", "telefono": "915 333 444",
     "categoria": "medico", "notas": "Para el control de la diabetes"},
    {"nombre": "Centro de salud", "telefono": "915 789 012",
     "categoria": "medico", "notas": ""},
    # Farmacia
    {"nombre": "Farmacia del barrio", "telefono": "915 444 555",
     "categoria": "farmacia", "notas": ""},
    # Otro
    {"nombre": "Fontanero (Pepe)", "telefono": "612 666 777",
     "categoria": "otro", "notas": "De confianza"},
]


def crear_contactos(mayor, lista):
    for c in lista:
        Contacto.objects.create(
            usuario_mayor=mayor,
            nombre=c["nombre"],
            telefono=c["telefono"],
            categoria=c["categoria"],
            notas=c["notas"],
        )


crear_contactos(carmen, contactos_carmen)
crear_contactos(antonio, contactos_antonio)
print(f"OK - Contactos: {len(contactos_carmen)} para Carmen, "
      f"{len(contactos_antonio)} para Antonio")


# ----------------------------------------------------------------------------
# 5. MENSAJES
# ----------------------------------------------------------------------------

Mensaje.objects.filter(
    remitente__in=[carmen, antonio, laura, miguel],
    destinatario__in=[carmen, antonio, laura, miguel],
).delete()

# Conversación Carmen <-> Laura (un par sin leer)
mensajes_carmen_laura = [
    (laura, carmen, "¡Hola mamá! ¿Cómo va el día?",
     now - timedelta(days=1, hours=3), True),
    (carmen, laura, "Hola hija, todo bien. Hoy he ido al mercado.",
     now - timedelta(days=1, hours=2, minutes=45), True),
    (laura, carmen, "Genial. Acuérdate del cardiólogo el miércoles.",
     now - timedelta(days=1, hours=2), True),
    (carmen, laura, "Sí, lo tengo apuntado. Gracias por recordármelo.",
     now - timedelta(days=1, hours=1, minutes=50), True),
    # Mensajes recientes SIN LEER para Carmen
    (laura, carmen, "Te he añadido la cita del análisis para el lunes.",
     now - timedelta(hours=2), False),
    (laura, carmen, "Avísame si necesitas que te acompañe.",
     now - timedelta(hours=1, minutes=55), False),
]

# Conversación Antonio <-> Laura
mensajes_antonio_laura = [
    (laura, antonio, "Papá, ¿has tomado la pastilla del azúcar?",
     now - timedelta(days=1, hours=5), True),
    (antonio, laura, "Sí, hace un rato. Gracias hija.",
     now - timedelta(days=1, hours=4, minutes=50), True),
    # Mensaje reciente SIN LEER para Antonio
    (miguel, antonio, "¡Papá! El sábado vamos a comer todos a casa.",
     now - timedelta(hours=3), False),
]

# Conversación Carmen <-> Antonio (matrimonio chateando entre ellos)
mensajes_matrimonio = [
    (carmen, antonio, "Antonio, ¿has visto las llaves?",
     now - timedelta(days=2, hours=8), True),
    (antonio, carmen, "Están en la entrada, encima del mueble.",
     now - timedelta(days=2, hours=7, minutes=55), True),
]


def crear_mensajes(lista):
    for remitente, destinatario, texto, fecha, leido in lista:
        m = Mensaje.objects.create(
            remitente=remitente,
            destinatario=destinatario,
            texto=texto,
            leido=leido,
        )
        Mensaje.objects.filter(pk=m.pk).update(enviado_en=fecha)


crear_mensajes(mensajes_carmen_laura)
crear_mensajes(mensajes_antonio_laura)
crear_mensajes(mensajes_matrimonio)
print("OK - Mensajes creados con conversaciones realistas")


# ----------------------------------------------------------------------------
# 6. RESUMEN FINAL
# ----------------------------------------------------------------------------

print("")
print("=" * 70)
print("DATOS DE DEMOSTRACIÓN CREADOS CORRECTAMENTE")
print("=" * 70)
print(f"  Grupo familiar:  FAM-A3K9 (Familia González-Pérez)")
print(f"")
print(f"  Cuentas creadas:")
print(f"  - carmen   / Carmen2026    (mayor, 76)")
print(f"  - antonio  / Antonio2026   (mayor, 79)")
print(f"  - laura    / Laura2026     (editor, hija)")
print(f"  - miguel   / Miguel2026    (amigo, hijo)")
print(f"")
print(f"  Recordatorios: 6 para Carmen, 6 para Antonio (2 de hoy cada uno)")
print(f"  Contactos:     8 para Carmen, 7 para Antonio")
print(f"  Mensajes:      conversaciones realistas con algunos sin leer")
print(f"")
print(f"  Pendiente manual:")
print(f"  - Subir 5-6 fotos a la galería desde la app (cuenta de Laura)")
print("=" * 70)

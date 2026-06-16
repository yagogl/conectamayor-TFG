# ConectaMayor

Aplicación web accesible diseñada para facilitar la comunicación entre
personas mayores y sus familiares en un entorno digital sencillo, privado
y seguro.

Trabajo Fin de Grado del Grado en Ingeniería Informática de la Escuela
Politécnica Superior de la Universidad Autónoma de Madrid (EPS-UAM).

## Características

- Tres roles de usuario: persona mayor (interfaz simplificada), familiar
  editor (gestión completa) y familiar de solo lectura.
- Vinculación familiar mediante códigos de invitación.
- Módulos: agenda de recordatorios, contactos, mensajería uno a uno,
  galería de fotos compartida y subsistema de notificaciones.
- Diseño conforme a las pautas de accesibilidad WCAG 2.1 nivel AA.

## Tecnologías

- Python 3.12
- Django 6.0
- SQLite
- Bootstrap 5
- JavaScript (AJAX)

## Instalación y ejecución

1. Clonar el repositorio:

```bash
git clone https://github.com/yagogl/conectamayor-TFG.git
cd conectamayor
```

2. Crear y activar un entorno virtual:

```bash
python -m venv venv
source venv/bin/activate    # En Windows: venv\Scripts\activate
```

3. Instalar las dependencias:

```bash
pip install -r requirements.txt
```

4. Aplicar las migraciones de la base de datos:

```bash
python manage.py migrate
```

5. (Opcional) Cargar datos de demostración:

```bash
python manage.py shell < seed_demo.py
```

6. Crear un superusuario para acceder al panel de administración:

```bash
python manage.py createsuperuser
```

7. Iniciar el servidor de desarrollo:

```bash
python manage.py runserver
```

8. Abrir la aplicación en el navegador:

```
http://127.0.0.1:8000
```

## Estructura del proyecto

El proyecto se organiza en aplicaciones Django independientes:

- `usuarios`: autenticación, roles y grupos familiares.
- `agenda`: recordatorios.
- `contactos`: gestión de contactos.
- `mensajes`: mensajería uno a uno.
- `galeria`: fotografías compartidas.

## Autor

Yago Gamo López

## Licencia

Proyecto académico desarrollado como Trabajo Fin de Grado.

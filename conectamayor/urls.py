from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('usuarios.urls')),
    path('agenda/', include('agenda.urls')),
    path('contactos/', include('contactos.urls')),
    path('mensajes/', include('mensajes.urls')),
    path('galeria/', include('galeria.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

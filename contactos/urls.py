from django.urls import path
from . import views

app_name = 'contactos'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('nuevo/', views.nuevo_contacto, name='nuevo'),
    path('editar/<int:pk>/', views.editar_contacto, name='editar'),
    path('borrar/<int:pk>/', views.borrar_contacto, name='borrar'),
]

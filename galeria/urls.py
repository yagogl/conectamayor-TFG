from django.urls import path
from . import views

app_name = 'galeria'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('subir/', views.subir_foto, name='subir'),
    path('<int:pk>/', views.detalle_foto, name='detalle'),
    path('<int:pk>/borrar/', views.borrar_foto, name='borrar'),
]

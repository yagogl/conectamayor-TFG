from django.urls import path
from . import views

app_name = 'agenda'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('nuevo/', views.nuevo_recordatorio, name='nuevo'),
    path('editar/<int:pk>/', views.editar_recordatorio, name='editar'),
    path('borrar/<int:pk>/', views.borrar_recordatorio, name='borrar'),
    path('hecho/<int:pk>/', views.marcar_hecho, name='hecho'),
    path('mas-tarde/<int:pk>/', views.recordar_mas_tarde, name='mas_tarde'),
]

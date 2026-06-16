from django.urls import path
from . import views

app_name = 'mensajes'

urlpatterns = [
    path('', views.lista, name='lista'),
    path('<int:usuario_id>/', views.conversacion, name='conversacion'),
    path('<int:usuario_id>/nuevos/', views.mensajes_nuevos, name='nuevos'),
]

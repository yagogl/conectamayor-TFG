from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registro/', views.registro, name='registro'),
    path('unirse/', views.unirse_grupo, name='unirse_grupo'),
    path('inicio/mayor/', views.inicio_mayor, name='inicio_mayor'),
    path('inicio/familiar/', views.inicio_familiar, name='inicio_familiar'),
    path('perfil/', views.perfil, name='perfil'),
]

"""
URL configuration for residencia_estudiantil project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('', views.home_view, name='home'),  # Nueva ruta para el home
    path('logout/', views.logout_view, name='logout'),
    path('listar_apartamentos/', views.listar_apartamentos_view, name='listar_apartamentos'),  # Nueva ruta para listar apartamentos
    path('get_apartamento/<int:id>/', views.get_apartamento, name='get_apartamento'),  # Nueva ruta para obtener datos de apartamento
    path('delete_apartamento/<int:id>/', views.delete_apartamento, name='delete_apartamento'),  # Nueva ruta para eliminar apartamento
    path('add_becado/', views.add_becado_view, name='add_becado'),  # Nueva ruta para agregar becado
    path('list_residencias/', views.list_residencias_view, name='list_residencias'),  # Nueva ruta para listar residencias
    path('get_residencia/<int:id>/', views.get_residencia, name='get_residencia'),  # Nueva ruta para obtener datos de residencia
    path('delete_residencia/<int:id>/', views.delete_residencia, name='delete_residencia'),  # Nueva ruta para eliminar residencia
]

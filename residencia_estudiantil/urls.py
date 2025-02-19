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
    path('', views.home_view, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('listar_apartamentos/', views.listar_apartamentos_view, name='listar_apartamentos'),
    path('get_apartamento/<int:id>/', views.get_apartamento, name='get_apartamento'),
    path('delete_apartamento/<int:id>/', views.delete_apartamento, name='delete_apartamento'),
    path('add_becado/', views.add_becado_view, name='add_becado'),
    path('list_residencias/', views.list_residencias_view, name='list_residencias'),
    path('get_residencia/<int:id>/', views.get_residencia, name='get_residencia'),
    path('delete_residencia/<int:id>/', views.delete_residencia, name='delete_residencia'),
    path('get_becado/<int:id>/', views.get_becado, name='get_becado'),
    path('delete_becado/<int:id>/', views.delete_becado, name='delete_becado'),
    path('export_becados/', views.export_becados_view, name='export_becados'),
]

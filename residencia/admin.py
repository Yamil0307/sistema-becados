from django.contrib import admin
from .models import Residencia, Apartamento, Becado, BecadoExtranjero

@admin.register(Residencia)
class ResidenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'cantidad_apartamentos', 'jefe_consejo', 
                   'profesor_atiende', 'get_evaluacion_residencia')
    search_fields = ('nombre', 'jefe_consejo', 'profesor_atiende')

@admin.register(Apartamento)
class ApartamentoAdmin(admin.ModelAdmin):
    list_display = ('numero', 'residencia', 'cantidad_becados', 'jefe_apto', 
                   'profesor_atiende', 'get_evaluacion_apto')
    list_filter = ('residencia',)
    search_fields = ('numero', 'jefe_apto', 'profesor_atiende')

@admin.register(Becado)
class BecadoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_identidad', 'carrera', 'año', 'apartamento', 
                   'evaluacion_jefe_residencia', 'evaluacion_jefe_apto', 
                   'evaluacion_profesor', 'promedio_evaluacion', 'get_evaluacion_cualitativa')
    list_filter = ('apartamento__residencia', 'apartamento', 'carrera', 'año')
    search_fields = ('nombre', 'numero_identidad', 'carrera')
    ordering = ('nombre',)

@admin.register(BecadoExtranjero)
class BecadoExtranjeroAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'numero_identidad', 'carrera', 'año', 'apartamento',
                   'pais_procedencia', 'numero_pasaporte', 'año_entrada',
                   'evaluacion_jefe_residencia', 'evaluacion_jefe_apto',
                   'evaluacion_profesor', 'evaluacion_relaciones_internacionales',
                   'promedio_evaluacion', 'get_evaluacion_cualitativa')
    list_filter = ('apartamento__residencia', 'apartamento', 'carrera', 'año',
                  'pais_procedencia')
    search_fields = ('nombre', 'numero_identidad', 'numero_pasaporte',
                    'pais_procedencia', 'carrera')
    ordering = ('nombre',)

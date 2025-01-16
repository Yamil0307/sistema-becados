from django import forms
from .models import Apartamento, Becado, Residencia

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = ['residencia', 'numero', 'cantidad_becados', 'jefe_apto', 'profesor_atiende']

class BecadoForm(forms.ModelForm):
    class Meta:
        model = Becado
        fields = [
            'nombre', 
            'numero_identidad', 
            'direccion_particular',
            'carrera', 
            'año', 
            'apartamento',
            'pais',
            'evaluacion_jefe_residencia',
            'evaluacion_jefe_apto',
            'evaluacion_profesor'
        ]

class ResidenciaForm(forms.ModelForm):
    class Meta:
        model = Residencia
        fields = ['nombre', 'cantidad_apartamentos', 'jefe_consejo', 'profesor_atiende']

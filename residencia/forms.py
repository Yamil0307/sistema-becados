from django import forms
from .models import Apartamento, Becado, Residencia

class ApartamentoForm(forms.ModelForm):
    class Meta:
        model = Apartamento
        fields = ['residencia', 'numero', 'cantidad_becados', 'capacidad', 'jefe_apto', 'profesor_atiende']

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

    def clean_numero_identidad(self):
        numero_identidad = self.cleaned_data.get('numero_identidad')
        if len(numero_identidad) != 11:
            raise forms.ValidationError("El número de identidad debe tener 11 dígitos.")
        return numero_identidad

class ResidenciaForm(forms.ModelForm):
    class Meta:
        model = Residencia
        fields = ['nombre', 'cantidad_apartamentos', 'jefe_consejo', 'profesor_atiende']

from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Count, Q

class Residencia(models.Model):
    nombre = models.CharField(max_length=100)
    cantidad_apartamentos = models.IntegerField()
    jefe_consejo = models.CharField(max_length=100)
    profesor_atiende = models.CharField(max_length=100)

    def get_evaluacion_residencia(self):
        # Obtener todos los apartamentos de la residencia
        total_aptos = self.apartamentos.count()
        if total_aptos == 0:
            return "Sin Evaluación"

        # Contar apartamentos por evaluación
        evaluaciones = {
            'Mal': self.apartamentos.filter(get_evaluacion_apto='Mal').count(),
            'Regular': self.apartamentos.filter(get_evaluacion_apto='Regular').count(),
            'Excelente': self.apartamentos.filter(get_evaluacion_apto='Excelente').count(),
        }

        # Calcular porcentajes
        porcentaje_mal = (evaluaciones['Mal'] / total_aptos) * 100
        porcentaje_regular = (evaluaciones['Regular'] / total_aptos) * 100

        # Si 5% o más están evaluados de Mal
        if porcentaje_mal >= 5:
            return "Mal"

        # Si el 100% está evaluado de Excelente
        if evaluaciones['Excelente'] == total_aptos:
            return "Excelente"

        # Si 30% o más están evaluados de Regular
        if porcentaje_regular >= 30:
            return "Regular"
        # Si menos del 30% está evaluado de Regular
        else:
            return "Bien"

    def __str__(self):
        return self.nombre

class Apartamento(models.Model):
    residencia = models.ForeignKey(Residencia, on_delete=models.CASCADE)
    numero = models.CharField(max_length=10)
    cantidad_becados = models.IntegerField()
    jefe_apto = models.CharField(max_length=100)
    profesor_atiende = models.CharField(max_length=100)

    def get_evaluacion_apto(self):
        # Obtener todos los becados del apartamento
        total_becados = self.becados.count()
        if total_becados == 0:
            return "Sin Evaluación"

        # Contar becados por evaluación
        evaluaciones = {
            'Mal': self.becados.filter(
                Q(get_evaluacion_cualitativa='Mal') |
                Q(becadoextranjero__get_evaluacion_cualitativa='Mal')
            ).count(),
            'Regular': self.becados.filter(
                Q(get_evaluacion_cualitativa='Regular') |
                Q(becadoextranjero__get_evaluacion_cualitativa='Regular')
            ).count(),
            'Excelente': self.becados.filter(
                Q(get_evaluacion_cualitativa='Excelente') |
                Q(becadoextranjero__get_evaluacion_cualitativa='Excelente')
            ).count(),
        }

        # Si hay al menos un estudiante evaluado de Mal
        if evaluaciones['Mal'] > 0:
            return "Mal"

        # Si el 100% está evaluado de Excelente
        if evaluaciones['Excelente'] == total_becados:
            return "Excelente"

        # Calcular porcentaje de Regular
        porcentaje_regular = (evaluaciones['Regular'] / total_becados) * 100

        # Si 30% o más están evaluados de Regular
        if porcentaje_regular >= 30:
            return "Regular"
        # Si menos del 30% está evaluado de Regular
        else:
            return "Bien"

    def __str__(self):
        return f"Apartamento {self.numero} - {self.residencia.nombre}"

class Becado(models.Model):
    apartamento = models.ForeignKey(Apartamento, on_delete=models.CASCADE, related_name='becados')
    nombre = models.CharField(max_length=200, verbose_name="Nombre completo")
    numero_identidad = models.CharField(max_length=11, unique=True, verbose_name="Número de identidad")
    direccion_particular = models.TextField(verbose_name="Dirección Particular")  # Nuevo campo
    año = models.PositiveIntegerField(verbose_name="Año que cursa")
    carrera = models.CharField(max_length=100, verbose_name="Carrera")
    evaluacion_jefe_residencia = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name="Evaluación del Jefe de Residencia"
    )
    evaluacion_jefe_apto = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name="Evaluación del Jefe de Apartamento"
    )
    evaluacion_profesor = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name="Evaluación del Profesor"
    )
    pais = models.CharField(max_length=100, verbose_name="País de Origen", default="Cuba")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Becado"
        verbose_name_plural = "Becados"
        ordering = ['nombre']

    def __str__(self):
        return f"{self.nombre} - {self.carrera} ({self.año}° año)"

    def promedio_evaluacion(self):
        return (self.evaluacion_jefe_residencia + 
                self.evaluacion_jefe_apto + 
                self.evaluacion_profesor) / 3

    def get_evaluacion_cualitativa(self):
        # Verificar si alguna evaluación es 2
        if (self.evaluacion_jefe_residencia == 2 or 
            self.evaluacion_jefe_apto == 2 or 
            self.evaluacion_profesor == 2):
            return "Mal"
        
        # Calcular promedio
        promedio = self.promedio_evaluacion()
        
        if promedio > 4.75:
            return "Excelente"
        elif 4 <= promedio <= 4.75:
            return "Bien"
        elif 3 <= promedio < 4:
            return "Regular"
        else:
            return "Mal"

class BecadoExtranjero(Becado):
    pais_procedencia = models.CharField(max_length=100, verbose_name="País de Procedencia")
    numero_pasaporte = models.CharField(max_length=50, unique=True, verbose_name="Número de Pasaporte")
    direccion_embajada = models.TextField(verbose_name="Dirección de la Embajada")
    año_entrada = models.PositiveIntegerField(verbose_name="Año de Entrada al País")
    evaluacion_relaciones_internacionales = models.IntegerField(
        validators=[MinValueValidator(2), MaxValueValidator(5)],
        verbose_name="Evaluación del Jefe de Relaciones Internacionales"
    )

    class Meta:
        verbose_name = "Becado Extranjero"
        verbose_name_plural = "Becados Extranjeros"

    def promedio_evaluacion(self):
        promedio_base = super().promedio_evaluacion()
        return (promedio_base * 3 + self.evaluacion_relaciones_internacionales) / 4

    def get_evaluacion_cualitativa(self):
        # Verificar si alguna evaluación es 2
        if (self.evaluacion_jefe_residencia == 2 or 
            self.evaluacion_jefe_apto == 2 or 
            self.evaluacion_profesor == 2 or 
            self.evaluacion_relaciones_internacionales == 2):
            return "Mal"
        
        # Calcular promedio
        promedio = self.promedio_evaluacion()
        
        if promedio > 4.75:
            return "Excelente"
        elif 4 <= promedio <= 4.75:
            return "Bien"
        elif 3 <= promedio < 4:
            return "Regular"
        else:
            return "Mal"

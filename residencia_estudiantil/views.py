import os
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from residencia.forms import ApartamentoForm, BecadoForm, ResidenciaForm
from residencia.models import Residencia, Apartamento, Becado

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirigir a la página principal después del login
        else:
            messages.error(request, 'Usuario o contraseña incorrectos')
    
    return render(request, 'login.html')

@login_required
def home_view(request):
    return render(request, 'home.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Has cerrado sesión correctamente')
    return redirect('login')

@login_required
def listar_apartamentos_view(request):
    evaluation_filter = request.GET.get('evaluation_filter', 'all')
    mal_filter = request.GET.get('mal_filter', 'off')

    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento_id')
        if apartamento_id:
            apartamento = get_object_or_404(Apartamento, id=apartamento_id)
            form = ApartamentoForm(request.POST, instance=apartamento)
            if form.is_valid():
                form.save()
                messages.success(request, 'Apartamento editado exitosamente')
            else:
                messages.error(request, 'Error al editar el apartamento')
        else:
            form = ApartamentoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Apartamento agregado exitosamente')
            else:
                messages.error(request, 'Error al agregar el apartamento')
        return redirect('listar_apartamentos')
    else:
        form = ApartamentoForm()

    apartamentos = Apartamento.objects.all()
    for apto in apartamentos:
        apto.actualizar_cantidad_becados()

    if evaluation_filter != 'all':
        apartamentos = [apto for apto in apartamentos if apto.get_evaluacion_apto() == evaluation_filter]

    if mal_filter == 'on':
        apartamentos = [apto for apto in apartamentos if sum(1 for becado in apto.becados.all() if becado.get_evaluacion_cualitativa() == 'Mal') > 2]

    count = len(apartamentos)

    return render(request, 'listar_apartamentos.html', {'form': form, 'apartamentos': apartamentos, 'evaluation_filter': evaluation_filter, 'mal_filter': mal_filter, 'count': count})

@login_required
def get_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    data = {
        'residencia': apartamento.residencia.id,
        'numero': apartamento.numero,
        'cantidad_becados': apartamento.cantidad_becados,
        'capacidad': apartamento.capacidad,  # Nuevo campo
        'jefe_apto': apartamento.jefe_apto,
        'profesor_atiende': apartamento.profesor_atiende,
    }
    return JsonResponse(data)

@login_required
def delete_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    if request.method == 'DELETE':
        apartamento.delete()
        return HttpResponse(status=204)
    return HttpResponse(status=405)

@login_required
def add_becado_view(request):
    filter_option = request.GET.get('filter_option', 'all')
    filter_country = request.GET.get('filter_country', '')
    evaluation_filter = request.GET.get('evaluation_filter', 'all')
    birthday_month = request.GET.get('birthday_month', '')

    if filter_option == 'foreign':
        becados = Becado.objects.exclude(pais='Cuba').order_by('nombre')
    elif filter_option == 'country' and filter_country:
        becados = Becado.objects.filter(pais__icontains=filter_country).order_by('nombre')
    else:
        becados = Becado.objects.all().order_by('nombre')

    if evaluation_filter != 'all':
        becados = [becado for becado in becados if becado.get_evaluacion_cualitativa() == evaluation_filter]

    if birthday_month:
        becados = [becado for becado in becados if becado.numero_identidad[2:4] == birthday_month]

    if request.method == 'POST':
        becado_id = request.POST.get('becado_id')
        if becado_id:
            becado = get_object_or_404(Becado, id=becado_id)
            form = BecadoForm(request.POST, instance=becado)
            if form.is_valid():
                form.save()
                messages.success(request, 'Becado editado exitosamente')
                return redirect('add_becado')
        else:
            form = BecadoForm(request.POST)
            if form.is_valid():
                try:
                    becado = form.save(commit=False)
                    apartamento = becado.apartamento
                    if apartamento.cantidad_becados < apartamento.capacidad:  # Comprobar capacidad disponible
                        apartamento.cantidad_becados += 1
                        apartamento.save()
                        becado.save()
                        messages.success(request, 'Becado agregado exitosamente')
                        return redirect('add_becado')
                    else:
                        messages.error(request, 'El apartamento no tiene capacidad disponible')
                except Exception as e:
                    messages.error(request, f'Error al guardar el becado: {str(e)}')
            else:
                messages.error(request, 'Por favor, corrija los errores en el formulario')
    else:
        form = BecadoForm()
    
    return render(request, 'add_becado.html', {'form': form, 'becados': becados, 'filter_option': filter_option, 'filter_country': filter_country, 'evaluation_filter': evaluation_filter, 'birthday_month': birthday_month})

@login_required
def list_residencias_view(request):
    if request.method == 'POST':
        residencia_id = request.POST.get('residencia_id')
        if residencia_id:
            residencia = get_object_or_404(Residencia, id=residencia_id)
            form = ResidenciaForm(request.POST, instance=residencia)
            if form.is_valid():
                form.save()
                messages.success(request, 'Residencia editada exitosamente')
        else:
            form = ResidenciaForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Residencia agregada exitosamente')
        return redirect('list_residencias')
    else:
        form = ResidenciaForm()

    residencias = Residencia.objects.all()
    residencia_data = []

    for residencia in residencias:
        cubanos = Becado.objects.filter(apartamento__residencia=residencia, pais='Cuba').count()
        extranjeros = Becado.objects.filter(apartamento__residencia=residencia).exclude(pais='Cuba').count()
        evaluacion = calcular_evaluacion_residencia(residencia)
        residencia_data.append({
            'residencia': residencia,
            'cubanos': cubanos,
            'extranjeros': extranjeros,
            'evaluacion': evaluacion
        })

    return render(request, 'list_residencias.html', {'residencias': residencia_data, 'form': form})

def calcular_evaluacion_residencia(residencia):
    becados = Becado.objects.filter(apartamento__residencia=residencia)
    if not becados:
        return "Sin Evaluación"
    evaluaciones = [becado.get_evaluacion_cualitativa() for becado in becados]
    # Implementar lógica para calcular la evaluación de la residencia
    # Por ejemplo, podrías calcular la evaluación promedio o usar otra lógica
    # Aquí se muestra un ejemplo simple de cómo podrías hacerlo
    if evaluaciones.count("Excelente") > evaluaciones.count("Mal"):
        return "Excelente"
    elif evaluaciones.count("Bien") > evaluaciones.count("Regular"):
        return "Bien"
    elif evaluaciones.count("Regular") > evaluaciones.count("Mal"):
        return "Regular"
    else:
        return "Mal"

@login_required
def get_residencia(request, id):
    residencia = get_object_or_404(Residencia, id=id)
    data = {
        'nombre': residencia.nombre,
        'cantidad_apartamentos': residencia.cantidad_apartamentos,
        'jefe_consejo': residencia.jefe_consejo,
        'profesor_atiende': residencia.profesor_atiende,
    }
    return JsonResponse(data)

@login_required
def delete_residencia(request, id):
    residencia = get_object_or_404(Residencia, id=id)
    if request.method == 'DELETE':
        residencia.delete()
        return HttpResponse(status=204)
    return HttpResponse(status=405)

@login_required
def get_becado(request, id):
    becado = get_object_or_404(Becado, id=id)
    data = {
        'nombre': becado.nombre,
        'numero_identidad': becado.numero_identidad,
        'direccion_particular': becado.direccion_particular,
        'carrera': becado.carrera,
        'año': becado.año,
        'apartamento': becado.apartamento.id,
        'pais': becado.pais,
        'evaluacion_jefe_residencia': becado.evaluacion_jefe_residencia,
        'evaluacion_jefe_apto': becado.evaluacion_jefe_apto,
        'evaluacion_profesor': becado.evaluacion_profesor,
    }
    return JsonResponse(data)

def listar_becados_view(request):
    if request.method == 'POST':
        becado_id = request.POST.get('becado_id')
        if becado_id:
            becado = get_object_or_404(Becado, id=becado_id)
            form = BecadoForm(request.POST, instance=becado)
            if form.is_valid():
                form.save()
                messages.success(request, 'Becado editado exitosamente')
            else:
                messages.error(request, 'Error al editar el becado')
        else:
            form = BecadoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Becado agregado exitosamente')
            else:
                messages.error(request, 'Error al agregar el becado')
        return redirect('listar_becados')
    else:
        form = BecadoForm()
    
    becados = Becado.objects.all()
    return render(request, 'listar_becados.html', {'form': form, 'becados': becados})

@login_required
def delete_becado(request, id):
    becado = get_object_or_404(Becado, id=id)
    apartamento = becado.apartamento
    if request.method == 'POST':
        becado.delete()
        apartamento.cantidad_becados -= 1
        apartamento.save()
        messages.success(request, 'Becado eliminado exitosamente')
        return redirect('add_becado')
    return HttpResponse(status=405)

@login_required
def export_becados_view(request):
    filter_option = request.GET.get('filter_option', 'all')
    filter_country = request.GET.get('filter_country', '')
    filename = request.GET.get('filename', 'becados_evaluacion.txt')

    if not filename.endswith('.txt'):
        filename += '.txt'

    if filter_option == 'foreign':
        becados = Becado.objects.exclude(pais='Cuba').order_by('nombre')
    elif filter_option == 'country' and filter_country:
        becados = Becado.objects.filter(pais__icontains=filter_country).order_by('nombre')
    else:
        becados = Becado.objects.all().order_by('nombre')

    file_path = os.path.join(settings.BASE_DIR, filename)
    with open(file_path, 'w') as file:
        for becado in becados:
            file.write(f'{becado.nombre}: {becado.get_evaluacion_cualitativa()}\n')
    messages.success(request, f'Listado de becados exportado exitosamente como {filename}')
    return redirect('add_becado')

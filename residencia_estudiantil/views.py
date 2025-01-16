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
    if request.method == 'POST':
        apartamento_id = request.POST.get('apartamento_id')
        if apartamento_id:
            apartamento = get_object_or_404(Apartamento, id=apartamento_id)
            form = ApartamentoForm(request.POST, instance=apartamento)
            if form.is_valid():
                form.save()
                messages.success(request, 'Apartamento editado exitosamente')
        else:
            form = ApartamentoForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Apartamento agregado exitosamente')
        return redirect('listar_apartamentos')
    else:
        form = ApartamentoForm()
    
    apartamentos = Apartamento.objects.all()
    return render(request, 'listar_apartamentos.html', {'form': form, 'apartamentos': apartamentos})

@login_required
def get_apartamento(request, id):
    apartamento = get_object_or_404(Apartamento, id=id)
    data = {
        'residencia': apartamento.residencia.id,
        'numero': apartamento.numero,
        'cantidad_becados': apartamento.cantidad_becados,
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
    if request.method == 'POST':
        form = BecadoForm(request.POST)
        if form.is_valid():
            try:
                becado = form.save(commit=False)
                apartamento = becado.apartamento
                if apartamento.cantidad_becados < 4:  # Suponiendo que la capacidad máxima es 4
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
    
    becados = Becado.objects.all().order_by('nombre')
    return render(request, 'add_becado.html', {'form': form, 'becados': becados})

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
    return render(request, 'list_residencias.html', {'residencias': residencias, 'form': form})

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

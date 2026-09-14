from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Assessor
from .forms import CadastrarAssessorForm, EditarAssessorForm
from apps.finance.decorators import cargo_requerido


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.role == user.Role.ASSESSOR:
                return redirect("dashboard:assessor")

            elif user.role == user.Role.FINANCEIRO:
                return redirect("dashboard:financeiro")

    else:
        form = AuthenticationForm()

    context = {"form": form}
    
    return render(request, "accounts/login.html", context)


def logout_view(request):
    logout(request)
    return redirect("accounts:login")


@cargo_requerido('financeiro')
@login_required
def listar_assessores(request):
    if request.method == "POST":
        form = CadastrarAssessorForm(request.POST)
        
        if form.is_valid():
            assessor = form.save()
            messages.success(request, f"Assessor {assessor.user.get_full_name() or assessor.user.username} cadastrado com sucesso!")
            return redirect("accounts:listar_assessores")
    else:
        form = CadastrarAssessorForm()
    
    assessores = Assessor.objects.select_related("user").order_by("user__first_name")
    
    context = {"form": form, "assessores": assessores}
    
    return render(request, "accounts/gestao_assessores.html", context)


@cargo_requerido('financeiro')
@login_required
def editar_assessor(request, pk):
    assessor = get_object_or_404(Assessor.objects.select_related("user"), pk=pk)
    
    if request.method == "POST":
        form = EditarAssessorForm(request.POST, assessor=assessor)
        
        if form.is_valid():
            form.save()
            messages.success(request, f"Dados do assessor {assessor.user.get_full_name()} atualizados com sucesso!")
            return redirect("accounts:listar_assessores")
    else:
        form = EditarAssessorForm(assessor=assessor)
    
    context = {"form": form, "assessor": assessor}

    return render(request, "accounts/editar_assessor.html", context)


@cargo_requerido('financeiro')
@login_required
def excluir_assessor(request, pk):
    assessor = get_object_or_404(Assessor.objects.select_related("user"), pk=pk)
    if request.method == "POST":
        user = assessor.user
        nome = user.get_full_name() or user.username
        
        # Ao deletar o CustomUser, o Assessor (e em cascata suas comissões) é deletado
        user.delete()
        messages.success(request, f"Assessor {nome} foi excluído com sucesso!")
        return redirect("accounts:listar_assessores")
    return redirect("accounts:editar_assessor", pk=pk)

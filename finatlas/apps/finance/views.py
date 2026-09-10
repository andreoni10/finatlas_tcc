import datetime
from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from apps.accounts.models import Assessor
from .forms import LancamentoPJ2SeguroForm, LancamentoPJ2ConsorcioForm, LancamentoPlusForm, ImportarPJ1Form, ImportarPJ2Form, FechamentoMensalForm
from .models import LancamentoPJ2Seguro, LancamentoPJ2Consorcio, LancamentoPlus, LancamentoPJ1, LancamentoPJ2Previdencia, FechamentoMensalAssessor
from .services import importar_excel_pj1, importar_excel_pj2, gerar_ou_atualizar_fechamento
from .decorators import cargo_requerido


@cargo_requerido('financeiro')
@login_required
def lancamentos_manuais(request):
    form_seguro = LancamentoPJ2SeguroForm(prefix="seguro")
    form_consorcio = LancamentoPJ2ConsorcioForm(prefix="consorcio")
    form_plus = LancamentoPlusForm(prefix="plus")
    form_pj1 = ImportarPJ1Form(prefix="pj1")
    form_pj2 = ImportarPJ2Form(prefix="pj2")
    
    if request.method == "POST":
        action = request.POST.get("action")
        if action == "salvar_seguro":
            salvar_seguro(request, form_seguro)
            return redirect("finance:lancamentos_manuais")
        elif action == "salvar_consorcio":
            salvar_consorcio(request, form_consorcio)
            return redirect("finance:lancamentos_manuais")
        elif action == "salvar_plus":
            salvar_plus(request, form_plus)
            return redirect("finance:lancamentos_manuais")
        elif action == "salvar_pj1":
            salvar_pj1(request, form_pj1)
            return redirect("finance:lancamentos_manuais")
        elif action == "salvar_pj2":
            salvar_pj2(request, form_pj2)
            return redirect("finance:lancamentos_manuais")
    
    # Busca os últimos lançamentos para exibição
    ultimos_seguros = LancamentoPJ2Seguro.objects.select_related("assessor__user").order_by("-id")[:5]
    ultimos_consorcio = LancamentoPJ2Consorcio.objects.select_related("assessor__user").order_by("-id")[:5]
    ultimos_plus = LancamentoPlus.objects.select_related("assessor__user").order_by("-id")[:5]
    ultimos_pj1 = LancamentoPJ1.objects.select_related("assessor__user").order_by("-id")[:5]
    ultimos_pj2 = LancamentoPJ2Previdencia.objects.select_related("assessor__user").order_by("-id")[:5]
    
    context = {
        "form_seguro": form_seguro,
        "form_consorcio": form_consorcio,
        "form_plus": form_plus,
        "form_pj1": form_pj1,
        "form_pj2": form_pj2,
        "ultimos_seguros": ultimos_seguros,
        "ultimos_consorcio": ultimos_consorcio,
        "ultimos_plus": ultimos_plus,
        "ultimos_pj1": ultimos_pj1,
        "ultimos_pj2": ultimos_pj2,
    }
    
    return render(request, "finance/lancamentos_manuais.html", context)


def salvar_seguro(request, form_seguro):
    form_seguro = LancamentoPJ2SeguroForm(request.POST, prefix="seguro")
            
    if form_seguro.is_valid():
        seguro = form_seguro.save(commit=False)
        seguro.comissao_assessor_60 = seguro.comissao_bruta_escritorio * Decimal("0.60") # Cálculo automatico de 60% para o assessor
        seguro.save()
        messages.success(request, f"Seguro de {seguro.cliente} ({seguro.seguradora}) cadastrado com sucesso!")


def salvar_consorcio(request, form_consorcio):
    form_consorcio = LancamentoPJ2ConsorcioForm(request.POST, prefix="consorcio")
            
    if form_consorcio.is_valid():
        consorcio = form_consorcio.save(commit=False)
        consorcio.comissao_assessor_60 = consorcio.comissao_bruta_escritorio * Decimal("0.60") # Cálculo automatico de 60% para o assessor
        consorcio.save()
        messages.success(request, f"Consórcio de {consorcio.cliente} ({consorcio.administradora}) cadastrado com sucesso!")


def salvar_plus(request, form_plus):
    form_plus = LancamentoPlusForm(request.POST, prefix="plus")
            
    if form_plus.is_valid():
        plus = form_plus.save(commit=False)
        plus.valor_imposto = plus.valor_bruto * (plus.pct_imposto / Decimal("100")) # Cálculo automático do imposto e líquido
        plus.valor_liquido = plus.valor_bruto - plus.valor_imposto
        plus.save()
        messages.success(request, f"Lançamento da Plus ({plus.parceiro}) cadastrado com sucesso!")


def salvar_pj1(request, form_pj1):
    form_pj1 = ImportarPJ1Form(request.POST, request.FILES, prefix="pj1")
    
    if form_pj1.is_valid():
        data = form_pj1.cleaned_data["data"]
        arquivo_pj1 = form_pj1.cleaned_data["arquivo_pj1"]
        try:
            total = importar_excel_pj1(arquivo_pj1, data_competencia=data)
            if total > 0:
                messages.success(request, f"Sucesso! {total} linhas de PJ1 foram importadas e salvas.")
            else:
                messages.warning(request, "O arquivo foi lido, mas nenhuma linha coincidiu com o código dos assessores cadastrados.")
        except Exception as e:
            messages.error(request, f"Erro ao ler arquivo Excel: {e}")


def salvar_pj2(request, form_pj2):
    form_pj2 = ImportarPJ2Form(request.POST, request.FILES, prefix="pj2")
    
    if form_pj2.is_valid():
        data = form_pj2.cleaned_data["data"]
        arquivo_pj2 = form_pj2.cleaned_data["arquivo_pj2"]
        try:
            total = importar_excel_pj2(arquivo_pj2, data_competencia=data)
            if total > 0:
                messages.success(request, f"Sucesso! {total} linhas de PJ2 foram importadas e salvas.")
            else:
                messages.warning(request, "O arquivo foi lido, mas nenhuma linha coincidiu com os assessores cadastrados.")
        except Exception as e:
            messages.error(request, f"Erro ao ler arquivo PJ2: {e}")


@cargo_requerido('financeiro')
@login_required
def gestao_fechamento(request):
    hoje = datetime.date.today()
    mes = int(request.GET.get("mes", hoje.month))
    ano = int(request.GET.get("ano", hoje.year))
    assessor_id = request.GET.get("assessor_id")

    assessores = Assessor.objects.select_related("user").filter(is_active=True).order_by("user__first_name")
    
    assessor_selecionado = None
    fechamento = None
    form = None

    if assessor_id:
        assessor_selecionado = Assessor.objects.filter(pk=assessor_id).first()
        
        if assessor_selecionado:
            # Puxa os brutos das tabelas ou pega o existente
            fechamento = gerar_ou_atualizar_fechamento(assessor_selecionado, ano, mes)

            if request.method == "POST":
                form = FechamentoMensalForm(request.POST, instance=fechamento)
                if form.is_valid():
                    form.save()
                    messages.success(request, f"Fechamento de {assessor_selecionado} atualizado com sucesso!")
                    return redirect(f"{request.path}?assessor_id={assessor_id}&mes={mes}&ano={ano}")
            else:
                form = FechamentoMensalForm(instance=fechamento)

    meses = [
        {"num": 1, "nome": "Janeiro"},
        {"num": 2, "nome": "Fevereiro"}, 
        {"num": 3, "nome": "Março"},
        {"num": 4, "nome": "Abril"}, 
        {"num": 5, "nome": "Maio"}, 
        {"num": 6, "nome": "Junho"},
        {"num": 7, "nome": "Julho"}, 
        {"num": 8, "nome": "Agosto"}, 
        {"num": 9, "nome": "Setembro"},
        {"num": 10, "nome": "Outubro"}, 
        {"num": 11, "nome": "Novembro"}, 
        {"num": 12, "nome": "Dezembro"}
    ]
    
    anos = [ano, ano - 1, ano - 2]

    context = {
        "assessores": assessores,
        "assessor_selecionado": assessor_selecionado,
        "fechamento": fechamento,
        "form": form,
        "mes_selecionado": mes,
        "ano_selecionado": ano,
        "meses": meses,
        "anos": anos,
    }
    
    return render(request, "finance/gestao_fechamento.html", context)

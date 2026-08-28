import datetime
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render
from apps.accounts.models import Assessor
from apps.finance.models import (
    LancamentoPJ1,
    LancamentoPJ2Previdencia,
    LancamentoPJ2Seguro,
    LancamentoPJ2Consorcio,
    LancamentoPlus,
)
from .decorators import cargo_requerido


@cargo_requerido("assessor")
@login_required
def advisor_dashboard(request):
    """
    Dashboard do Assessor com isolamento de dados e filtro por mês/ano.
    """
    try:
        assessor = request.user.advisor_profile
    except Assessor.DoesNotExist:
        return render(request, "dashboard/dashboard_assessor.html", {"sem_perfil": True})
    # Pega o mês e ano do filtro (ou usa o mês/ano atual por padrão)
    hoje = datetime.date.today()
    mes = int(request.GET.get("mes", hoje.month))
    ano = int(request.GET.get("ano", hoje.year))
    # Consultas filtradas estritamente para o assessor logado
    pj1_itens = LancamentoPJ1.objects.filter(
        assessor=assessor, data__year=ano, data__month=mes
    )
    pj2_prev_itens = LancamentoPJ2Previdencia.objects.filter(
        assessor=assessor, data__year=ano, data__month=mes
    )
    pj2_seg_itens = LancamentoPJ2Seguro.objects.filter(
        assessor=assessor, data__year=ano, data__month=mes
    )
    pj2_con_itens = LancamentoPJ2Consorcio.objects.filter(
        assessor=assessor, data__year=ano, data__month=mes
    )
    plus_itens = LancamentoPlus.objects.filter(
        assessor=assessor, data__year=ano, data__month=mes
    )
    # Cálculos dos Totais
    total_pj1 = pj1_itens.aggregate(total=Sum("comissao_assessor"))["total"] or 0
    total_pj2_prev = pj2_prev_itens.aggregate(total=Sum("comissao_assessor_60"))["total"] or 0
    total_pj2_seg = pj2_seg_itens.aggregate(total=Sum("comissao_assessor_60"))["total"] or 0
    total_pj2_con = pj2_con_itens.aggregate(total=Sum("comissao_assessor_60"))["total"] or 0
    total_pj2 = float(total_pj2_prev) + float(total_pj2_seg) + float(total_pj2_con)
    total_plus = plus_itens.aggregate(total=Sum("valor_liquido"))["total"] or 0
    total_geral = float(total_pj1) + float(total_pj2) + float(total_plus)
    # Lista de meses para o select
    meses_disponiveis = [
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
        {"num": 12, "nome": "Dezembro"},
    ]
    anos_disponiveis = [ano, ano - 1, ano - 2]
    context = {
        "assessor": assessor,
        "mes_selecionado": mes,
        "ano_selecionado": ano,
        "meses": meses_disponiveis,
        "anos": anos_disponiveis,
        "total_geral": total_geral,
        "total_pj1": total_pj1,
        "total_pj2": total_pj2,
        "total_pj2_prev": total_pj2_prev,
        "total_pj2_seg": total_pj2_seg,
        "total_pj2_con": total_pj2_con,
        "total_plus": total_plus,
        "pj1_itens": pj1_itens,
        "pj2_prev_itens": pj2_prev_itens,
        "pj2_seg_itens": pj2_seg_itens,
        "pj2_con_itens": pj2_con_itens,
        "plus_itens": plus_itens,
    }
    return render(request, "dashboard/dashboard_assessor.html", context)


@cargo_requerido("financeiro")
@login_required
def finance_dashboard(request):
    return render(request, "dashboard/dashboard_financeiro.html")

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
    FechamentoMensalAssessor,
)
from .decorators import cargo_requerido
from apps.finance.services import gerar_ou_atualizar_fechamento


@cargo_requerido("assessor")
@login_required
def advisor_dashboard(request):
    # Pegar o assessor logado
    try:
        assessor = request.user.advisor_profile
    except Assessor.DoesNotExist:
        return render(request, "dashboard/dashboard_assessor.html", {"sem_perfil": True})
    
    # Pega o mês e ano do filtro (ou usa o mês/ano atual por padrão)
    hoje = datetime.date.today()
    mes = int(request.GET.get("mes", hoje.month))
    ano = int(request.GET.get("ano", hoje.year))

    # Gera ou obtém o fechamento oficial do assessor
    gerar_ou_atualizar_fechamento(assessor, ano, mes)
    fechamento = FechamentoMensalAssessor.objects.get(
        assessor=assessor,
        competencia=datetime.date(ano, mes, 1),
    )
    
    # Consultas filtradas estritamente para o assessor logado
    pj1_itens = LancamentoPJ1.objects.filter(assessor=assessor, data__year=ano, data__month=mes)
    pj2_prev_itens = LancamentoPJ2Previdencia.objects.filter(assessor=assessor, data__year=ano, data__month=mes)
    pj2_seg_itens = LancamentoPJ2Seguro.objects.filter(assessor=assessor, data__year=ano, data__month=mes)
    pj2_con_itens = LancamentoPJ2Consorcio.objects.filter(assessor=assessor, data__year=ano, data__month=mes)
    plus_itens = LancamentoPlus.objects.filter(assessor=assessor, data__year=ano, data__month=mes)
    
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
    
    # Busca todos os anos com lançamentos para o assessor
    anos_comissao = set()
    modelos = [
        LancamentoPJ1,
        LancamentoPJ2Previdencia,
        LancamentoPJ2Seguro,
        LancamentoPJ2Consorcio,
        LancamentoPlus,
    ]
    for model in modelos:
        anos_encontrados = model.objects.filter(assessor=assessor).values_list("data__year", flat=True).distinct()
        anos_comissao.update(filter(None, anos_encontrados))

    # Garante o ano atual na lista para o assessor sempre poder consultar o ano corrente
    anos_comissao.add(hoje.year)

    # Pega do ano mais recente (max) ao mais antigo (min)
    ano_recente = max(anos_comissao)
    ano_antigo = min(anos_comissao)

    # Gera a lista em ordem decrescente (ex: de 2026 até 2021)
    anos_disponiveis = list(range(ano_recente, ano_antigo - 1, -1))
    
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
        "fechamento": fechamento,
    }
    
    return render(request, "dashboard/dashboard_assessor.html", context)


import json


@cargo_requerido("financeiro")
@login_required
def finance_dashboard(request):
    hoje = datetime.date.today()
    ano_selecionado = int(request.GET.get("ano", hoje.year))
    
    mes_param = request.GET.get("mes", "")
    mes_selecionado = int(mes_param) if mes_param.isdigit() and 1 <= int(mes_param) <= 12 else None

    # 1. Anos disponíveis
    anos_comissao = set()
    modelos = [
        LancamentoPJ1,
        LancamentoPJ2Previdencia,
        LancamentoPJ2Seguro,
        LancamentoPJ2Consorcio,
        LancamentoPlus,
    ]
    for model in modelos:
        anos_encontrados = model.objects.values_list("data__year", flat=True).distinct()
        anos_comissao.update(filter(None, anos_encontrados))
    anos_comissao.add(hoje.year)
    anos_disponiveis = list(range(max(anos_comissao), min(anos_comissao) - 1, -1))

    # Nomes dos meses
    meses_nomes = [
        "Jan", "Fev", "Mar", "Abr", "Mai", "Jun",
        "Jul", "Ago", "Set", "Out", "Nov", "Dez"
    ]
    meses_filtro = [
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

    # 2. Inicializar séries mensais (1 a 12)
    faturamento_mensal_pj1 = [0.0] * 12
    faturamento_mensal_pj2 = [0.0] * 12
    faturamento_mensal_plus = [0.0] * 12
    comissao_mensal_assessores = [0.0] * 12

    # PJ1 no ano
    pj1_ano = LancamentoPJ1.objects.filter(data__year=ano_selecionado)
    for row in pj1_ano.values("data__month").annotate(
        fat=Sum("comissao_bruta_escritorio"),
        com=Sum("comissao_assessor"),
    ):
        m = row["data__month"]
        if 1 <= m <= 12:
            faturamento_mensal_pj1[m - 1] += float(row["fat"] or 0)
            comissao_mensal_assessores[m - 1] += float(row["com"] or 0)

    # PJ2 Previdência no ano
    pj2_prev_ano = LancamentoPJ2Previdencia.objects.filter(data__year=ano_selecionado)
    for row in pj2_prev_ano.values("data__month").annotate(
        fat=Sum("comissao_escritorio"),
        com=Sum("comissao_assessor_60"),
    ):
        m = row["data__month"]
        if 1 <= m <= 12:
            faturamento_mensal_pj2[m - 1] += float(row["fat"] or 0)
            comissao_mensal_assessores[m - 1] += float(row["com"] or 0)

    # PJ2 Seguro no ano
    pj2_seg_ano = LancamentoPJ2Seguro.objects.filter(data__year=ano_selecionado)
    for row in pj2_seg_ano.values("data__month").annotate(
        fat=Sum("comissao_bruta_escritorio"),
        com=Sum("comissao_assessor_60"),
    ):
        m = row["data__month"]
        if 1 <= m <= 12:
            faturamento_mensal_pj2[m - 1] += float(row["fat"] or 0)
            comissao_mensal_assessores[m - 1] += float(row["com"] or 0)

    # PJ2 Consórcio no ano
    pj2_con_ano = LancamentoPJ2Consorcio.objects.filter(data__year=ano_selecionado)
    for row in pj2_con_ano.values("data__month").annotate(
        fat=Sum("comissao_bruta_escritorio"),
        com=Sum("comissao_assessor_60"),
    ):
        m = row["data__month"]
        if 1 <= m <= 12:
            faturamento_mensal_pj2[m - 1] += float(row["fat"] or 0)
            comissao_mensal_assessores[m - 1] += float(row["com"] or 0)

    # Plus no ano
    plus_ano = LancamentoPlus.objects.filter(data__year=ano_selecionado)
    for row in plus_ano.values("data__month").annotate(
        fat=Sum("valor_bruto"),
        com=Sum("valor_liquido"),
    ):
        m = row["data__month"]
        if 1 <= m <= 12:
            faturamento_mensal_plus[m - 1] += float(row["fat"] or 0)
            comissao_mensal_assessores[m - 1] += float(row["com"] or 0)

    # Totais consolidados do escritório (ano ou mês filtrado)
    if mes_selecionado:
        total_pj1 = faturamento_mensal_pj1[mes_selecionado - 1]
        total_pj2 = faturamento_mensal_pj2[mes_selecionado - 1]
        total_plus = faturamento_mensal_plus[mes_selecionado - 1]
        total_comissoes = comissao_mensal_assessores[mes_selecionado - 1]
    else:
        total_pj1 = sum(faturamento_mensal_pj1)
        total_pj2 = sum(faturamento_mensal_pj2)
        total_plus = sum(faturamento_mensal_plus)
        total_comissoes = sum(comissao_mensal_assessores)

    total_faturamento = total_pj1 + total_pj2 + total_plus
    retencao_escritorio = total_faturamento - total_comissoes

    # 3. Comissionamento Bruto e Líquido por Assessor (Mensal e Anual)
    assessores = Assessor.objects.select_related("user").all()

    # Mapeamentos mensais por assessor para performance O(1)
    pj1_mes_assessor = {
        (row["assessor_id"], row["data__month"]): float(row["total"] or 0)
        for row in pj1_ano.values("assessor_id", "data__month").annotate(total=Sum("comissao_assessor"))
    }
    pj2_prev_mes_assessor = {
        (row["assessor_id"], row["data__month"]): float(row["total"] or 0)
        for row in pj2_prev_ano.values("assessor_id", "data__month").annotate(total=Sum("comissao_assessor_60"))
    }
    pj2_seg_mes_assessor = {
        (row["assessor_id"], row["data__month"]): float(row["total"] or 0)
        for row in pj2_seg_ano.values("assessor_id", "data__month").annotate(total=Sum("comissao_assessor_60"))
    }
    pj2_con_mes_assessor = {
        (row["assessor_id"], row["data__month"]): float(row["total"] or 0)
        for row in pj2_con_ano.values("assessor_id", "data__month").annotate(total=Sum("comissao_assessor_60"))
    }
    plus_mes_assessor = {
        (row["assessor_id"], row["data__month"]): float(row["total"] or 0)
        for row in plus_ano.values("assessor_id", "data__month").annotate(total=Sum("valor_liquido"))
    }

    fechamentos_map = {
        (f.assessor_id, f.competencia.month): f
        for f in FechamentoMensalAssessor.objects.filter(competencia__year=ano_selecionado)
    }

    dados_assessores = []

    for a in assessores:
        meses_extrato = []
        total_bruto_ano = 0.0
        total_liquido_ano = 0.0

        for m in range(1, 13):
            # Se houver fechamento mensal oficial gerado/editado pela financeira
            fech = fechamentos_map.get((a.id, m))
            if fech:
                p1 = float(fech.pj1_bruto)
                p2 = float(fech.pj2_bruto)
                pl = float(fech.plus_bruto)
                bruto_m = float(fech.total_bruto)
                liquido_m = float(fech.total_liquido)
            else:
                p1 = pj1_mes_assessor.get((a.id, m), 0.0)
                p2 = (
                    pj2_prev_mes_assessor.get((a.id, m), 0.0)
                    + pj2_seg_mes_assessor.get((a.id, m), 0.0)
                    + pj2_con_mes_assessor.get((a.id, m), 0.0)
                )
                pl = plus_mes_assessor.get((a.id, m), 0.0)
                bruto_m = p1 + p2 + pl
                # Alíquotas padrão de imposto (14.66% PJ1 e PJ2, 6.00% Plus)
                liquido_m = (p1 * 0.8534) + (p2 * 0.8534) + (pl * 0.94)

            total_bruto_ano += bruto_m
            total_liquido_ano += liquido_m

            meses_extrato.append({
                "mes_num": m,
                "mes_nome": meses_nomes[m - 1],
                "pj1_bruto": round(p1, 2),
                "pj2_bruto": round(p2, 2),
                "plus_bruto": round(pl, 2),
                "total_bruto": round(bruto_m, 2),
                "total_liquido": round(liquido_m, 2),
                "tem_movimento": (bruto_m > 0 or liquido_m > 0),
            })

        # Define valores a exibir na visualização ativa (mês filtrado ou ano consolidado)
        if mes_selecionado:
            item_sel = meses_extrato[mes_selecionado - 1]
            pj1_exibido = item_sel["pj1_bruto"]
            pj2_exibido = item_sel["pj2_bruto"]
            plus_exibido = item_sel["plus_bruto"]
            bruto_exibido = item_sel["total_bruto"]
            liquido_exibido = item_sel["total_liquido"]
        else:
            pj1_exibido = round(sum(item["pj1_bruto"] for item in meses_extrato), 2)
            pj2_exibido = round(sum(item["pj2_bruto"] for item in meses_extrato), 2)
            plus_exibido = round(sum(item["plus_bruto"] for item in meses_extrato), 2)
            bruto_exibido = round(total_bruto_ano, 2)
            liquido_exibido = round(total_liquido_ano, 2)

        nome = a.user.get_full_name() or a.user.username
        dados_assessores.append({
            "id": a.id,
            "nome": nome,
            "codigo": a.codigo_assessor,
            "is_active": a.is_active,
            "pj1": pj1_exibido,
            "pj2": pj2_exibido,
            "plus": plus_exibido,
            "bruto": bruto_exibido,
            "liquido": liquido_exibido,
            "total_bruto_ano": round(total_bruto_ano, 2),
            "total_liquido_ano": round(total_liquido_ano, 2),
            "meses_extrato": meses_extrato,
        })

    # Ordenar assessores por nome
    dados_assessores.sort(key=lambda x: x["nome"])

    # Top assessores para o gráfico (até 10 maiores do ano)
    top_com_comissao = sorted([a for a in dados_assessores if a["total_bruto_ano"] > 0], key=lambda x: x["total_bruto_ano"], reverse=True)[:10]
    top_assessores = top_com_comissao if top_com_comissao else dados_assessores[:10]

    ranking_nomes = [a["nome"] for a in top_assessores]
    ranking_valores = [a["total_bruto_ano"] for a in top_assessores]

    # Nome do mês selecionado por extenso (se houver)
    nome_mes_selecionado = ""
    if mes_selecionado:
        nome_mes_selecionado = meses_filtro[mes_selecionado - 1]["nome"]

    context = {
        "ano_selecionado": ano_selecionado,
        "mes_selecionado": mes_selecionado,
        "nome_mes_selecionado": nome_mes_selecionado,
        "anos_disponiveis": anos_disponiveis,
        "meses_filtro": meses_filtro,
        "total_anual_faturamento": total_faturamento,
        "total_anual_pj1": total_pj1,
        "total_anual_pj2": total_pj2,
        "total_anual_plus": total_plus,
        "total_anual_comissoes": total_comissoes,
        "retencao_escritorio": retencao_escritorio,
        "dados_assessores": dados_assessores,
        # JSON para ApexCharts
        "meses_nomes_json": json.dumps(meses_nomes),
        "fat_pj1_json": json.dumps([round(x, 2) for x in faturamento_mensal_pj1]),
        "fat_pj2_json": json.dumps([round(x, 2) for x in faturamento_mensal_pj2]),
        "fat_plus_json": json.dumps([round(x, 2) for x in faturamento_mensal_plus]),
        "comissao_mensal_json": json.dumps([round(x, 2) for x in comissao_mensal_assessores]),
        "ranking_nomes_json": json.dumps(ranking_nomes),
        "ranking_valores_json": json.dumps(ranking_valores),
    }

    return render(request, "dashboard/dashboard_financeiro.html", context)

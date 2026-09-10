from django.contrib import admin
from .models import LancamentoPJ1, LancamentoPJ2Previdencia, LancamentoPJ2Seguro, LancamentoPJ2Consorcio, LancamentoPlus, FechamentoMensalAssessor


@admin.register(LancamentoPJ1)
class LancamentoPJ1Admin(admin.ModelAdmin):
    list_display = ["produto", "assessor", "cod_cliente", "receita_liquida", "comissao_assessor", "data"]
    list_filter = ["data", "categoria", "assessor"]
    search_fields = ["produto", "cod_cliente", "cod_assessor_direto"]


@admin.register(LancamentoPJ2Previdencia)
class LancamentoPJ2PrevAdmin(admin.ModelAdmin):
    list_display = ["categoria", "assessor", "codigo_cliente", "receita_liquida", "comissao_escritorio", "data"]
    list_filter = ["data", "classificacao", "assessor"]
    search_fields = ["categoria", "codigo_cliente", "codigo_assessor"]


@admin.register(LancamentoPJ2Seguro)
class LancamentoPJ2SeguroAdmin(admin.ModelAdmin):
    list_display = ["seguradora", "cliente", "assessor", "comissao_bruta_escritorio", "comissao_assessor_60", "data"]
    list_filter = ["seguradora", "data", "assessor"]
    search_fields = ["cliente"]


@admin.register(LancamentoPJ2Consorcio)
class LancamentoPJ2ConsorcioAdmin(admin.ModelAdmin):
    list_display = ["administradora", "cliente", "assessor", "comissao_bruta_escritorio", "comissao_assessor_60", "data"]
    list_filter = ["administradora", "data", "assessor"]
    search_fields = ["cliente"]


@admin.register(LancamentoPlus)
class LancamentoPlusAdmin(admin.ModelAdmin):
    list_display = ["parceiro", "produto", "assessor", "valor_bruto", "valor_liquido", "data"]
    list_filter = ["parceiro", "data", "assessor"]
    search_fields = ["produto", "parceiro"]


@admin.register(FechamentoMensalAssessor)
class FechamentoMensalAssessorAdmin(admin.ModelAdmin):
    list_display = [
        "assessor",
        "competencia",
        "data_pagamento",
        "total_bruto",
        "total_imposto",
        "total_liquido",
    ]
    list_filter = ["competencia", "assessor"]
    search_fields = [
        "assessor__codigo_assessor",
        "assessor__user__first_name",
        "assessor__user__last_name",
        "assessor__user__username",
    ]
    # Campos que o método save() calcula sozinho e que podemos exibir como somente leitura
    readonly_fields = [
        "pj1_imposto",
        "pj1_liquido",
        "pj2_imposto",
        "pj2_liquido",
        "plus_imposto",
        "plus_liquido",
        "total_bruto",
        "total_imposto",
        "total_liquido",
        "criado_em",
        "atualizado_em",
    ]
    fieldsets = (
        (
            "Identificação & Competência",
            {
                "fields": ("assessor", "competencia", "data_pagamento"),
            },
        ),
        (
            "Accanto Assessoria (PJ1)",
            {
                "fields": (
                    "pj1_bruto",
                    "pct_imposto_pj1",
                    "pj1_imposto",
                    "pj1_liquido",
                ),
            },
        ),
        (
            "Accanto Serviços (PJ2)",
            {
                "fields": (
                    "pj2_bruto",
                    "pct_imposto_pj2",
                    "pj2_imposto",
                    "pj2_liquido",
                ),
            },
        ),
        (
            "PLUS (PJ3)",
            {
                "fields": (
                    "plus_bruto",
                    "pct_imposto_plus",
                    "plus_imposto",
                    "plus_liquido",
                ),
            },
        ),
        (
            "Deduções e Ajustes Líquidos Manuais",
            {
                "fields": (
                    "plano_saude",
                    "outros_creditos",
                    "outros_debitos",
                ),
            },
        ),
        (
            "Totais Consolidados",
            {
                "fields": (
                    "total_bruto",
                    "total_imposto",
                    "total_liquido",
                ),
            },
        ),
        (
            "Observações e Auditoria",
            {
                "fields": ("observacoes", "criado_em", "atualizado_em"),
            },
        ),
    )
from django.contrib import admin
from .models import LancamentoPJ1, LancamentoPJ2Previdencia, LancamentoPJ2Seguro, LancamentoPlus


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


@admin.register(LancamentoPlus)
class LancamentoPlusAdmin(admin.ModelAdmin):
    list_display = ["parceiro", "produto", "assessor", "valor_bruto", "valor_liquido", "data"]
    list_filter = ["parceiro", "data", "assessor"]
    search_fields = ["produto", "parceiro"]

from django.db import models
from apps.accounts.models import Assessor


class LancamentoPJ1(models.Model):
    # Vincula este lançamento ao Assessor dono da comissão
    assessor = models.ForeignKey(
        Assessor, on_delete=models.CASCADE, verbose_name="Assessor"
    )
    data = models.DateField("Data / Mês de Referência")

    # Colunas de texto que vêm do Excel
    categoria = models.CharField("Categoria", max_length=100, blank=True, default="")
    produto = models.CharField("Produto", max_length=150)
    nivel_1 = models.CharField("Nível 1", max_length=100, blank=True, default="")
    nivel_2 = models.CharField("Nível 2", max_length=100, blank=True, default="")
    nivel_3 = models.CharField("Nível 3", max_length=100, blank=True, default="")
    cod_cliente = models.CharField(
        "Cód. Cliente", max_length=50, blank=True, default=""
    )
    cod_assessor_direto = models.CharField("Cód. Assessor Direto", max_length=50)

    # Colunas de valores em dinheiro e porcentagens
    receita = models.DecimalField(
        "Receita (R$)", max_digits=12, decimal_places=2, default=0
    )
    receita_liquida = models.DecimalField(
        "Receita Líquida (R$)", max_digits=12, decimal_places=2, default=0
    )
    repasse_escritorio = models.DecimalField(
        "Repasse (%) Escritório", max_digits=5, decimal_places=2, default=0
    )
    comissao_bruta_escritorio = models.DecimalField(
        "Comissão Bruta (R$) Escritório", max_digits=12, decimal_places=2, default=0
    )
    repasse_assessor = models.DecimalField(
        "Repasse (%) Assessor", max_digits=5, decimal_places=2, default=0
    )
    comissao_assessor = models.DecimalField(
        "Comissão (R$) Assessor Direto", max_digits=12, decimal_places=2, default=0
    )

    def __str__(self):
        return f"PJ1 - {self.produto} - R$ {self.comissao_assessor}"


class LancamentoPJ2Previdencia(models.Model):
    assessor = models.ForeignKey(
        Assessor, on_delete=models.CASCADE, verbose_name="Assessor"
    )
    data = models.DateField("Data / Mês de Referência")

    # Colunas de texto do Excel
    classificacao = models.CharField(
        "Classificação", max_length=100, blank=True, default=""
    )
    categoria = models.CharField("Categoria", max_length=100, blank=True, default="")
    nivel_1 = models.CharField("Nível 1", max_length=100, blank=True, default="")
    nivel_2 = models.CharField("Nível 2", max_length=100, blank=True, default="")
    nivel_3 = models.CharField("Nível 3", max_length=100, blank=True, default="")
    nivel_4 = models.CharField("Nível 4", max_length=100, blank=True, default="")
    codigo_cliente = models.CharField(
        "Código Cliente", max_length=50, blank=True, default=""
    )
    codigo_assessor = models.CharField("Código Assessor", max_length=50)

    # Valores em dinheiro e comissões
    receita_bruta = models.DecimalField(
        "Receita Bruta", max_digits=12, decimal_places=2, default=0
    )
    receita_liquida = models.DecimalField(
        "Receita Líquida", max_digits=12, decimal_places=2, default=0
    )
    comissao_pct_escritorio = models.DecimalField(
        "Comissão (%) Escritório", max_digits=5, decimal_places=2, default=0
    )
    comissao_escritorio = models.DecimalField(
        "Comissão Escritório", max_digits=12, decimal_places=2, default=0
    )

    def __str__(self):
        return f"PJ2 Prev - {self.categoria} - R$ {self.comissao_escritorio}"


class LancamentoPJ2Seguro(models.Model):
    assessor = models.ForeignKey(
        Assessor, on_delete=models.CASCADE, verbose_name="Assessor"
    )
    data = models.DateField("Data")
    seguradora = models.CharField(
        "Seguradora", max_length=50
    )  # Ex: PRUDENTIAL, METLIFE, ICATU
    cliente = models.CharField("Cliente", max_length=150)
    comissao_bruta_escritorio = models.DecimalField(
        "Comissão Bruta (R$) Escritório", max_digits=12, decimal_places=2
    )
    comissao_assessor_60 = models.DecimalField(
        "Comissão Assessor 60%", max_digits=12, decimal_places=2
    )
    parcela = models.CharField("Parcela", max_length=20, default="1/1")

    def __str__(self):
        return f"Seguro {self.seguradora} - {self.cliente}"


class LancamentoPlus(models.Model):
    assessor = models.ForeignKey(
        Assessor, on_delete=models.CASCADE, verbose_name="Assessor"
    )
    data = models.DateField("Data")
    parceiro = models.CharField(
        "Parceiro", max_length=100
    )
    produto = models.CharField("Produto", max_length=150)
    valor_bruto = models.DecimalField(
        "Valor Bruto (R$)", max_digits=12, decimal_places=2
    )
    pct_imposto = models.DecimalField(
        "% Imposto", max_digits=5, decimal_places=2, default=0
    )
    valor_imposto = models.DecimalField(
        "Valor Imposto (R$)", max_digits=12, decimal_places=2, default=0
    )
    valor_liquido = models.DecimalField(
        "Valor Líquido (R$)", max_digits=12, decimal_places=2, default=0
    )

    def __str__(self):
        return f"Plus - {self.parceiro} - R$ {self.valor_liquido}"

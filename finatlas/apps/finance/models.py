from django.db import models
from apps.accounts.models import Assessor
from decimal import Decimal


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

    def save(self, *args, **kwargs):
        if self.receita_liquida and self.repasse_assessor:
            rec = Decimal(str(self.receita_liquida))
            rep = Decimal(str(self.repasse_assessor))
            self.comissao_assessor = (rec * (rep / Decimal("100"))).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)



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
    comissao_assessor_60 = models.DecimalField(
        "Comissão Assessor 60%", max_digits=12, decimal_places=2, default=0
    )

    def __str__(self):
        return f"PJ2 Prev - {self.categoria} - R$ {self.comissao_assessor_60}"


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
    parcela = models.CharField("Parcela", max_length=20)

    def __str__(self):
        return f"Seguro {self.seguradora} - {self.cliente}"
    
    def save(self, *args, **kwargs):
        bruta = Decimal(str(self.comissao_bruta_escritorio or 0))
        self.comissao_assessor_60 = (bruta * Decimal("0.60")).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)



class LancamentoPJ2Consorcio(models.Model):
    assessor = models.ForeignKey(
        Assessor, on_delete=models.CASCADE, verbose_name="Assessor"
    )
    data = models.DateField("Data")
    administradora = models.CharField(
        "Administradora", max_length=50
    )  # Ex: MAPFRE, CNP, EMBRACON
    cliente = models.CharField("Cliente", max_length=150)
    comissao_bruta_escritorio = models.DecimalField(
        "Comissão Bruta (R$) Escritório", max_digits=12, decimal_places=2
    )
    comissao_assessor_60 = models.DecimalField(
        "Comissão Assessor 60%", max_digits=12, decimal_places=2
    )
    parcela = models.CharField("Parcela", max_length=20)

    def __str__(self):
        return f"Seguro {self.administradora} - {self.cliente}"

    def save(self, *args, **kwargs):
        bruta = Decimal(str(self.comissao_bruta_escritorio or 0))
        self.comissao_assessor_60 = (bruta * Decimal("0.60")).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        bruto = Decimal(str(self.valor_bruto or 0))
        pct = Decimal(str(self.pct_imposto or 0))
        self.valor_imposto = (bruto * (pct / Decimal("100"))).quantize(Decimal("0.01"))
        self.valor_liquido = (bruto - self.valor_imposto).quantize(Decimal("0.01"))
        super().save(*args, **kwargs)



class FechamentoMensalAssessor(models.Model):
    assessor = models.ForeignKey(
        Assessor, on_delete=models.CASCADE, verbose_name="Assessor", related_name="fechamentos"
    )
    competencia = models.DateField("Competência (Mês/Ano)", db_index=True)
    data_pagamento = models.DateField("Data do Pagamento", null=True, blank=True)

    # Accanto Assessoria (PJ1)
    pj1_bruto = models.DecimalField("PJ1 Valor Bruto", max_digits=12, decimal_places=2, default=0.00)
    pct_imposto_pj1 = models.DecimalField("% Imposto PJ1", max_digits=5, decimal_places=2, default=14.66)
    pj1_imposto = models.DecimalField("PJ1 Valor Imposto", max_digits=12, decimal_places=2, default=0.00)
    pj1_liquido = models.DecimalField("PJ1 Valor Líquido", max_digits=12, decimal_places=2, default=0.00)

    # Accanto Serviços (PJ2)
    pj2_bruto = models.DecimalField("PJ2 Valor Bruto", max_digits=12, decimal_places=2, default=0.00)
    pct_imposto_pj2 = models.DecimalField("% Imposto PJ2", max_digits=5, decimal_places=2, default=14.66)
    pj2_imposto = models.DecimalField("PJ2 Valor Imposto", max_digits=12, decimal_places=2, default=0.00)
    pj2_liquido = models.DecimalField("PJ2 Valor Líquido", max_digits=12, decimal_places=2, default=0.00)

    # PLUS
    plus_bruto = models.DecimalField("PLUS Valor Bruto", max_digits=12, decimal_places=2, default=0.00)
    pct_imposto_plus = models.DecimalField("% Imposto PLUS", max_digits=5, decimal_places=2, default=6.00)
    plus_imposto = models.DecimalField("PLUS Valor Imposto", max_digits=12, decimal_places=2, default=0.00)
    plus_liquido = models.DecimalField("PLUS Valor Líquido", max_digits=12, decimal_places=2, default=0.00)

    # Deduções e Ajustes Manuais
    plano_saude = models.DecimalField("Plano de Saúde (Débito)", max_digits=12, decimal_places=2, default=0.00)
    outros_creditos = models.DecimalField("Outros Créditos", max_digits=12, decimal_places=2, default=0.00)
    outros_debitos = models.DecimalField("Outros Débitos", max_digits=12, decimal_places=2, default=0.00)

    # Totais Gerais
    total_bruto = models.DecimalField("Total Bruto", max_digits=12, decimal_places=2, default=0.00)
    total_imposto = models.DecimalField("Total Imposto", max_digits=12, decimal_places=2, default=0.00)
    total_liquido = models.DecimalField("Total Líquido Final", max_digits=12, decimal_places=2, default=0.00)

    observacoes = models.TextField("Observações", blank=True, default="")
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Fechamento Mensal do Assessor"
        verbose_name_plural = "Fechamentos Mensais dos Assessores"
        unique_together = ("assessor", "competencia")
        ordering = ["-competencia", "assessor"]

    def __str__(self):
        return f"Fechamento {self.assessor} - {self.competencia.strftime('%m/%Y')} - Líquido: R$ {self.total_liquido}"

    def save(self, *args, **kwargs):
        # Garante que todos os campos estejam no tipo Decimal
        pj1_bruto = Decimal(str(self.pj1_bruto or 0))
        pj2_bruto = Decimal(str(self.pj2_bruto or 0))
        plus_bruto = Decimal(str(self.plus_bruto or 0))

        pct_pj1 = Decimal(str(self.pct_imposto_pj1 or 0))
        pct_pj2 = Decimal(str(self.pct_imposto_pj2 or 0))
        pct_plus = Decimal(str(self.pct_imposto_plus or 0))

        plano_saude = Decimal(str(self.plano_saude or 0))
        outros_creditos = Decimal(str(self.outros_creditos or 0))
        outros_debitos = Decimal(str(self.outros_debitos or 0))

        cem = Decimal("100")

        # 1. Calcula impostos e líquidos de cada empresa
        self.pj1_imposto = (pj1_bruto * (pct_pj1 / cem)).quantize(Decimal("0.01"))
        self.pj1_liquido = (pj1_bruto - self.pj1_imposto).quantize(Decimal("0.01"))

        self.pj2_imposto = (pj2_bruto * (pct_pj2 / cem)).quantize(Decimal("0.01"))
        self.pj2_liquido = (pj2_bruto - self.pj2_imposto).quantize(Decimal("0.01"))

        self.plus_imposto = (plus_bruto * (pct_plus / cem)).quantize(Decimal("0.01"))
        self.plus_liquido = (plus_bruto - self.plus_imposto).quantize(Decimal("0.01"))

        # 2. Total Bruto e Total Imposto
        self.total_bruto = pj1_bruto + pj2_bruto + plus_bruto
        self.total_imposto = self.pj1_imposto + self.pj2_imposto + self.plus_imposto

        # 3. Total Líquido Final
        soma_liquidos = self.pj1_liquido + self.pj2_liquido + self.plus_liquido
        self.total_liquido = (
            soma_liquidos - plano_saude + outros_creditos - outros_debitos
        ).quantize(Decimal("0.01"))

        super().save(*args, **kwargs)


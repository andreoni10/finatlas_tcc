from django import forms
from .models import LancamentoPJ2Seguro, LancamentoPJ2Consorcio, LancamentoPlus


class LancamentoPJ2SeguroForm(forms.ModelForm):
    # Lista fixa das 3 seguradoras
    SEGURADORAS = [
        ("PRUDENTIAL", "Prudential"),
        ("METLIFE", "MetLife"),
        ("ICATU", "Icatu"),
    ]
    seguradora = forms.ChoiceField(choices=SEGURADORAS, label="Seguradora")

    class Meta:
        model = LancamentoPJ2Seguro
        # o sistema ira calcular sozinho a comissao do assessor
        fields = ["assessor", "data", "seguradora", "cliente", "comissao_bruta_escritorio", "parcela"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilo visual moderno em todos os campos
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal focus:border-teal outline-none text-sm text-slate-800"
            })


class LancamentoPJ2ConsorcioForm(forms.ModelForm):
    # Lista fixa das 3 administradoras
    ADMINISTRADORAS = [
        ("MAPFRE", "Mapfre"),
        ("CNP", "CNP"),
        ("EMBRACON", "Embracon"),
    ]
    administradora = forms.ChoiceField(choices=ADMINISTRADORAS, label="Administradora")

    class Meta:
        model = LancamentoPJ2Consorcio
        # o sistema ira calcular sozinho a comissao do assessor
        fields = ["assessor", "data", "administradora", "cliente", "comissao_bruta_escritorio", "parcela"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Aplica estilo visual moderno em todos os campos
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal focus:border-teal outline-none text-sm text-slate-800"
            })


class LancamentoPlusForm(forms.ModelForm):
    # Lista fixa dos 14 parceiros
    PARCEIROS = [
        ("VIPMARES", "VIPMARES"),
        ("MD GARANTIDOR", "MD GARANTIDOR"),
        ("LMS/FOCUS", "LMS/FOCUS"),
        ("RODOBENS", "RODOBENS"),
        ("DUOPLAN", "DUOPLAN"),
        ("ESOLEN (FINEPE)", "ESOLEN (FINEPE)"),
        ("PRIMO PRECATÓRIOS", "PRIMO PRECATÓRIOS"),
        ("NEWAVE", "NEWAVE"),
        ("FINANC SAFRA", "FINANC SAFRA"),
        ("ESSENCIAL", "ESSENCIAL"),
        ("REAL CRED", "REAL CRED"),
        ("PREV", "PREV"),
        ("SORIA CAPITAL", "SORIA CAPITAL"),
        ("BV FINANCEIRA", "BV FINANCEIRA"),
    ]
    parceiro = forms.ChoiceField(choices=PARCEIROS, label="Parceiro")

    class Meta:
        model = LancamentoPlus
        # o sistema ira calcular sozinho o valor_imposto e o valor_liquido
        fields = ["assessor", "data", "parceiro", "produto", "valor_bruto", "pct_imposto"]
        widgets = {
            "data": forms.DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "w-full px-3 py-2 border border-slate-300 rounded-lg focus:ring-2 focus:ring-teal focus:border-teal outline-none text-sm text-slate-800"
            })


class ImportarPJ1Form(forms.Form):
    data = forms.DateField(
        label="Data de Competência (Mês de Referência)",
        widget=forms.DateInput(attrs={"type": "date", "class": "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"}),
    )
    arquivo_pj1 = forms.FileField(
        label="Arquivo Excel PJ1 (.xlsx)",
        widget=forms.FileInput(attrs={"accept": ".xlsx, .xls", "class": "w-full text-sm text-slate-500 border border-slate-300 rounded-lg p-2"}),
    )


class ImportarPJ2Form(forms.Form):
    data = forms.DateField(
        label="Data de Competência (Mês de Referência)",
        widget=forms.DateInput(attrs={"type": "date", "class": "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm"}),
    )
    arquivo_pj2 = forms.FileField(
        label="Arquivo Excel PJ2 (.xlsx)",
        help_text="Banco XP, Mercado Internacional ou XPCS",
        widget=forms.FileInput(attrs={"accept": ".xlsx, .xls", "class": "w-full text-sm text-slate-500 border border-slate-300 rounded-lg p-2"}),
    )

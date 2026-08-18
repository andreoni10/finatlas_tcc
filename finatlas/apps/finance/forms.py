from django import forms
from .models import LancamentoPJ2Seguro, LancamentoPlus


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
        # Note que não pedimos a "comissao_assessor_60" porque o sistema vai calcular sozinho!
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
        # Não pedimos valor_imposto nem valor_liquido porque calcularemos automaticamente!
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

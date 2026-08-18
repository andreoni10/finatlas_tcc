from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import LancamentoPJ2SeguroForm, LancamentoPlusForm
from .models import LancamentoPJ2Seguro, LancamentoPlus


@login_required
def lancamentos_manuais(request):
    form_seguro = LancamentoPJ2SeguroForm(prefix="seguro")
    form_plus = LancamentoPlusForm(prefix="plus")

    if request.method == "POST":
        action = request.POST.get("action")

        # Se clicou em Salvar Seguro
        if action == "salvar_seguro":
            form_seguro = LancamentoPJ2SeguroForm(request.POST, prefix="seguro")
            
            if form_seguro.is_valid():
                seguro = form_seguro.save(commit=False)
                seguro.comissao_assessor_60 = seguro.comissao_bruta_escritorio * Decimal("0.60") # Cálculo automatico de 60% para o assessor
                seguro.save()
                messages.success(request, f"Seguro de {seguro.cliente} ({seguro.seguradora}) cadastrado com sucesso!")
                return redirect("finance:lancamentos_manuais")

        # Se clicou em Salvar Plus
        elif action == "salvar_plus":
            form_plus = LancamentoPlusForm(request.POST, prefix="plus")
            
            if form_plus.is_valid():
                plus = form_plus.save(commit=False)
                plus.valor_imposto = plus.valor_bruto * (plus.pct_imposto / Decimal("100")) # Cálculo automático do imposto e líquido
                plus.valor_liquido = plus.valor_bruto - plus.valor_imposto
                plus.save()
                messages.success(request, f"Lançamento da Plus ({plus.parceiro}) cadastrado com sucesso!")
                return redirect("finance:lancamentos_manuais")

    # Busca os últimos 5 lançamentos de cada para exibir na tela
    ultimos_seguros = LancamentoPJ2Seguro.objects.select_related("assessor__user").order_by("-id")[:5]
    ultimos_plus = LancamentoPlus.objects.select_related("assessor__user").order_by("-id")[:5]

    context = {
        "form_seguro": form_seguro,
        "form_plus": form_plus,
        "ultimos_seguros": ultimos_seguros,
        "ultimos_plus": ultimos_plus,
    }
    return render(request, "finance/lancamentos_manuais.html", context)

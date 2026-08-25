from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .decorators import cargo_requerido


@cargo_requerido('assessor')
@login_required
def advisor_dashboard(request):
    return render(request, "dashboard/dashboard_assessor.html")


@cargo_requerido('financeiro')
@login_required
def finance_dashboard(request):
    return render(request, "dashboard/dashboard_financeiro.html")

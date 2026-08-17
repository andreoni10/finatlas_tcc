from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required(login_url="login")
def advisor_dashboard(request):
    return render(request, "dashboard/dashboard_assessor.html")


@login_required(login_url="login")
def finance_dashboard(request):
    return render(request, "dashboard/dashboard_financeiro.html")

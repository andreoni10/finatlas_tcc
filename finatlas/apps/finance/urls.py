from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("lancamentos/", views.lancamentos_manuais, name="lancamentos_manuais"),
    path("fechamento/", views.gestao_fechamento, name="gestao_fechamento")
]


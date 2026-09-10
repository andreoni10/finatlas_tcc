from django.urls import path
from . import views

app_name = "finance"

urlpatterns = [
    path("lancamentos/", views.lancamentos_manuais, name="lancamentos_manuais"),
    path("fechamento/", views.gestao_fechamento, name="gestao_fechamento"),
    path("editar-lancamentos/", views.listar_lancamentos_para_edicao, name="editar_lancamento"),
    path("editar-lancamentos/<str:tipo>/<int:pk>/", views.editar_item_lancamento, name="editar_item_lancamento"),
]


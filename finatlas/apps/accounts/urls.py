from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("financeiro/assessores/", views.listar_assessores, name="listar_assessores"),
    path("financeiro/assessores/<int:pk>/editar/", views.editar_assessor, name="editar_assessor"),
    path("financeiro/assessores/<int:pk>/excluir/", views.excluir_assessor, name="excluir_assessor"),
]

from django.urls import path

from . import views

app_name = "dashboard"


urlpatterns = [
    path('assessor/', views.advisor_dashboard, name="assessor"),
    path('financeiro/', views.finance_dashboard, name="financeiro"),
]

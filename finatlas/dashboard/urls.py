from django.urls import path

from . import views

app_name = "dashboard"


urlpatterns = [
    path('', views.advisor_dashboard, name="assessor"),
]

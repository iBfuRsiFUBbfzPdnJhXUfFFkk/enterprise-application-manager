from django.urls import path

from kpi.views import kpi_home_view

urlpatterns = [
    path('', kpi_home_view, name='kpi_home'),
]
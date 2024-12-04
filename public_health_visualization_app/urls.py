from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/chart-data', views.chart_data, name='chart_data'),
]
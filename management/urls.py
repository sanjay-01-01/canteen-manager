# management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dashboard, name='home_dashboard'), 
    path('canteen/<int:canteen_id>/', views.canteen_report, name='canteen_report'),
    # नया URL पाथ
    path('payroll/', views.payroll_summary, name='payroll_summary'), 
]
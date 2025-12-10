# management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dashboard, name='home_dashboard'), 
    path('report/canteen/<int:canteen_id>/summary/', views.canteen_summary_report, name='canteen_summary_report'),
    path('report/canteen/<int:canteen_id>/date/<str:date_str>/', views.canteen_detail_report, name='canteen_detail_report'),
    path('payroll/', views.payroll_summary, name='payroll_summary'), 
    path('get-canteen-data/', views.get_canteen_data, name='get_canteen_data'),
]
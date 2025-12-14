# management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_dashboard, name='home_dashboard'), 
    path('report/canteen/<int:canteen_id>/summary/', views.canteen_summary_report, name='canteen_summary_report'),
    path('report/canteen/<int:canteen_id>/date/<str:date_str>/', views.canteen_detail_report, name='canteen_detail_report'),
    path('payroll/', views.payroll_summary, name='payroll_summary'), 
    path('get-canteen-data/', views.get_canteen_data, name='get_canteen_data'),
    path('staff/<int:staff_id>/profile/', views.staff_profile_view, name='staff_profile'),
    path('staff/list/', views.staff_list_view, name='staff_list'),
    path('staff/<int:staff_id>/detail/', views.staff_detail_view, name='staff_detail'),
    path('export/expenses/', views.export_monthly_expenses, name='export_expenses'),
    path('staff/<int:staff_id>/print/', views.print_staff_ledger, name='print_staff_ledger'),
    path('staff/<int:staff_id>/add-payment/', views.add_staff_payment, name='add_staff_payment'),
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-daily-entry/', views.add_daily_entry, name='add_daily_entry'),
    path('add-consumption/', views.add_consumption, name='add_consumption'),
    path('report/consumption/', views.consumption_report, name='consumption_report'),
]
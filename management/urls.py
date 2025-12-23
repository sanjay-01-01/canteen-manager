# management/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # 1. Dashboard
    path('', views.home_dashboard, name='home_dashboard'), 
    
    # 2. Canteen Reports
    path('report/canteen/<int:canteen_id>/summary/', views.canteen_summary_report, name='canteen_summary_report'),
    path('report/canteen/<int:canteen_id>/date/<str:date_str>/', views.canteen_detail_report, name='canteen_detail_report'),
    
    # 3. Payroll (Conflict Theek Kar Diya)
    path('payroll/summary/', views.payroll_summary, name='payroll_summary'),
    path('payroll/generate/', views.generate_payroll, name='generate_payroll'),

    # 4. API
    path('get-canteen-data/', views.get_canteen_data, name='get_canteen_data'),

    # 5. Staff Management (Job Left wale link hata diye)
    path('staff/list/', views.staff_list, name='staff_list'),
    path('staff/add/', views.add_staff, name='add_staff'),
    
    path('staff/<int:staff_id>/profile/', views.staff_profile_view, name='staff_profile'),
    path('staff/<int:staff_id>/detail/', views.staff_detail_view, name='staff_detail'),
    path('staff/<int:staff_id>/print/', views.print_staff_ledger, name='print_staff_ledger'),
    
    # 6. Payments & Leave
    path('staff/<int:staff_id>/add-payment/', views.add_staff_payment, name='add_staff_payment'), # Name fix
    path('staff/apply-leave/', views.apply_leave, name='apply_leave'),
    path('staff/leave-history/', views.staff_leave_history, name='staff_leave_history'),

    # 7. Expense & Entries
    path('add-expense/', views.add_expense, name='add_expense'),
    path('add-daily-entry/', views.add_daily_entry, name='add_daily_entry'),
    path('add-consumption/', views.add_consumption, name='add_consumption'),
    
    # 8. Exports
    path('export/expenses/', views.export_monthly_expenses, name='export_expenses'),
    path('canteen/<int:canteen_id>/download-excel/', views.export_canteen_excel, name='export_canteen_excel'),
    path('report/consumption/', views.consumption_report, name='consumption_report'),
    # Staff Management section me:
    path('staff/ex-employees/', views.ex_staff_list, name='ex_staff_list'),
    path('staff/<int:staff_id>/left/', views.mark_staff_left, name='mark_staff_left'),
]
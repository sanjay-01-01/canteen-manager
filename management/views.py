# management/views.py

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Sum
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from .models import Canteen, Expense, Staff, SalaryPayment, StaffLeave

# ==========================================
# 1. डैशबोर्ड (Home Dashboard)
# ==========================================
def home_dashboard(request):
    # 1. Date logic
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month + relativedelta(months=1) - timedelta(days=1)

    # 2. Calculation logic (Monthly Expenses)
    monthly_expenses_sum = Expense.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    # 3. Monthly Payments (Salary)
    monthly_payments_sum = SalaryPayment.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).aggregate(total_paid=Sum('amount'))['total_paid'] or 0

    # 4. Total Advance Paid (All time)
    total_advance_paid = SalaryPayment.objects.filter(payment_type='Advance').aggregate(total_adv=Sum('amount'))['total_adv'] or 0

    # 5. Fetching Canteens and Staff Counts
    all_canteens = Canteen.objects.all().order_by('name') 
    total_canteens_count = Canteen.objects.count()
    total_staff_count = Staff.objects.count()

    # 6. Final Unified Context
    context = {
        'current_month': today.strftime("%B %Y"),
        'total_canteens': total_canteens_count,
        'total_staff': total_staff_count,
        'all_canteens': all_canteens,

        # Summary data
        'monthly_expenses_sum': monthly_expenses_sum,
        'monthly_payments_sum': monthly_payments_sum,
        'total_advance_paid': total_advance_paid, 
    }

    return render(request, 'management/dashboard.html', context)


# ==========================================
# 2. कैंटीन रिपोर्टिंग (Summary & Detailed)
# ==========================================

# A. समरी रिपोर्ट व्यू (तारीख के हिसाब से टोटल)
def canteen_summary_report(request, canteen_id):
    canteen = get_object_or_404(Canteen, pk=canteen_id)
    
    # खर्चों को तारीख के हिसाब से ग्रुप करें और टोटल निकालें
    daily_expenses = Expense.objects.filter(canteen=canteen) \
        .values('date') \
        .annotate(total_amount=Sum('amount')) \
        .order_by('-date')
        
    context = {
        'canteen': canteen,
        'daily_expenses': daily_expenses,
    }
    return render(request, 'management/canteen_summary_report.html', context)


# B. डिटेल रिपोर्ट व्यू (एक खास तारीख का पूरा ब्यौरा)
def canteen_detail_report(request, canteen_id, date_str):
    canteen = get_object_or_404(Canteen, pk=canteen_id)
    
    # उस तारीख के सारे खर्च लाएं
    expenses = Expense.objects.filter(canteen=canteen, date=date_str).order_by('id')
    
    # उस दिन का कुल टोटल
    total_amount = expenses.aggregate(Sum('amount'))['amount__sum'] or 0

    context = {
        'canteen': canteen,
        'expenses': expenses,
        'total_amount': total_amount,
        'report_date': date_str,
    }
    return render(request, 'management/canteen_detail_report.html', context)


# ==========================================
# 3. पेरोल रिपोर्ट (Payroll Summary)
# ==========================================
def payroll_summary(request):
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month + relativedelta(months=1) - relativedelta(days=1)

    all_staff = Staff.objects.all().order_by('canteen__name', 'name')
    payroll_data = []

    for staff in all_staff:
        # Advance Paid (Total)
        advance_paid = SalaryPayment.objects.filter(
            staff=staff,
            payment_type='Advance'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # Paid this month
        paid_this_month = SalaryPayment.objects.filter(
            staff=staff,
            date__gte=first_day_of_month,
            date__lte=last_day_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # Leaves calculation
        leaves_this_month_periods = StaffLeave.objects.filter(
            staff=staff,
            start_date__gte=first_day_of_month,
            end_date__lte=last_day_of_month
        )
        total_leaves = sum(leave.total_days() for leave in leaves_this_month_periods)

        payroll_data.append({
            'staff': staff,
            'canteen_name': staff.canteen.name if staff.canteen else 'N/A',
            'monthly_salary': staff.monthly_salary,
            'total_advance_paid': advance_paid,
            'paid_this_month': paid_this_month,
            'leaves_this_month': total_leaves,
        })

    context = {
        'payroll_data': payroll_data,
        'current_month': today.strftime("%B %Y"),
    }
    return render(request, 'management/payroll_summary.html', context)


# ==========================================
# 4. API (JavaScript के लिए डेटा)
# ==========================================
def get_canteen_data(request):
    # डेटाबेस से सभी कैंटीनों की ID और Billing Type लाओ
    canteens = Canteen.objects.all().values('id', 'billing_type')
    
    # इसे JSON डिक्शनरी में बदलो: { '1': 'DAILY', '2': 'MONTHLY', ... }
    data = {str(c['id']): c['billing_type'] for c in canteens}
    
    return JsonResponse(data)
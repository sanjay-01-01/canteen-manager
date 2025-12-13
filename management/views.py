from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from datetime import date, timedelta
import datetime # Date parsing ke liye zaroori
from dateutil.relativedelta import relativedelta
import csv

# Models & Forms Import
from .models import Canteen, Expense, Staff, SalaryPayment, StaffLeave, DailyEntry
from .forms import SalaryPaymentForm, ExpenseForm, DailyEntryForm

# ==========================================
# 1. डैशबोर्ड (Home Dashboard)
# ==========================================
@login_required
def home_dashboard(request):
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month + relativedelta(months=1) - timedelta(days=1)

    # --- Expense & Salary ---
    monthly_expenses_sum = Expense.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    monthly_salary_paid = SalaryPayment.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0

    total_outflow = monthly_expenses_sum + monthly_salary_paid

    # --- Income ---
    income_entries = DailyEntry.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    )
    
    total_cash = income_entries.aggregate(total=Sum('cash_received'))['total'] or 0
    total_online = income_entries.aggregate(total=Sum('online_received'))['total'] or 0
    total_income = total_cash + total_online 

    # --- Net Profit ---
    net_profit = total_income - total_outflow

    # --- Charts Data ---
    expense_categories = Expense.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).values('category').annotate(sum=Sum('amount')).order_by('-sum')

    pie_labels = []
    pie_data = []
    
    for item in expense_categories:
        pie_labels.append(item['category'])
        pie_data.append(float(item['sum']))

    if monthly_salary_paid > 0:
        pie_labels.append('Staff Salary')
        pie_data.append(float(monthly_salary_paid))

    # --- Context ---
    all_canteens = Canteen.objects.all().order_by('name') 
    total_canteens = Canteen.objects.count()
    total_staff = Staff.objects.count()

    context = {
        'current_month': today.strftime("%B %Y"),
        'total_canteens': total_canteens,
        'total_staff': total_staff,
        'all_canteens': all_canteens,
        'total_income': total_income,
        'total_expense': total_outflow,
        'net_profit': net_profit,
        'pie_labels': pie_labels,
        'pie_data': pie_data,
    }

    return render(request, 'management/dashboard.html', context)


# ==========================================
# 2. कैंटीन रिपोर्टिंग (Summary & Detailed)
# ==========================================
@login_required
def canteen_summary_report(request, canteen_id):
    canteen = get_object_or_404(Canteen, pk=canteen_id)
    
    # Date Filter
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    today = date.today()
    if start_date_str:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
    else:
        start_date = today.replace(day=1)

    if end_date_str:
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
    else:
        end_date = today

    # --- EXPENSE GROUPING ---
    raw_expenses = Expense.objects.filter(
        canteen=canteen, 
        date__range=[start_date, end_date]
    ).order_by('-date')

    expenses_grouped = {}
    for exp in raw_expenses:
        d = exp.date
        if d not in expenses_grouped:
            expenses_grouped[d] = {'date': d, 'total_amount': 0, 'items': []}
        
        expenses_grouped[d]['total_amount'] += exp.amount
        expenses_grouped[d]['items'].append(exp)
    
    final_expense_list = list(expenses_grouped.values())

    # --- INCOME GROUPING ---
    raw_incomes = DailyEntry.objects.filter(
        canteen=canteen, 
        date__range=[start_date, end_date]
    ).order_by('-date')

    incomes_grouped = {}
    for inc in raw_incomes:
        d = inc.date
        if d not in incomes_grouped:
            incomes_grouped[d] = {'date': d, 'total_income': 0, 'cash': 0, 'online': 0}
        
        total = inc.cash_received + inc.online_received
        incomes_grouped[d]['total_income'] += total
        incomes_grouped[d]['cash'] += inc.cash_received
        incomes_grouped[d]['online'] += inc.online_received

    final_income_list = list(incomes_grouped.values())

    # --- Grand Totals ---
    total_income_sum = sum(item['total_income'] for item in final_income_list)
    total_expense_sum = sum(item['total_amount'] for item in final_expense_list)
    net_profit = total_income_sum - total_expense_sum

    context = {
        'canteen': canteen,
        'expense_list': final_expense_list,
        'income_list': final_income_list,
        'total_income': total_income_sum,
        'total_expense': total_expense_sum,
        'net_profit': net_profit,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'management/canteen_summary_report.html', context)

@login_required
def canteen_detail_report(request, canteen_id, date_str):
    canteen = get_object_or_404(Canteen, pk=canteen_id)
    expenses = Expense.objects.filter(canteen=canteen, date=date_str).order_by('id')
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
@login_required
def payroll_summary(request):
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month + relativedelta(months=1) - relativedelta(days=1)

    all_staff = Staff.objects.all().order_by('canteen__name', 'name')
    payroll_data = []

    for staff in all_staff:
        advance_paid = SalaryPayment.objects.filter(
            staff=staff,
            payment_type='Advance'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        paid_this_month = SalaryPayment.objects.filter(
            staff=staff,
            date__gte=first_day_of_month,
            date__lte=last_day_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

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
@login_required
def get_canteen_data(request):
    canteens = Canteen.objects.all().values('id', 'billing_type')
    data = {str(c['id']): c['billing_type'] for c in canteens}
    return JsonResponse(data)


# ==========================================
# 5. स्टाफ प्रोफाइल व्यू (Bank Passbook Style)
# ==========================================
@login_required
def staff_profile_view(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    
    start_filter = request.GET.get('start_date')
    end_filter = request.GET.get('end_date')

    loop_start_date = staff.joining_date if staff.joining_date else date(date.today().year, 1, 1)
    today = date.today()

    all_transactions = []

    # 1. Payments (Debit)
    payments = SalaryPayment.objects.filter(staff=staff)
    for pay in payments:
        all_transactions.append({
            'date': pay.date,
            'description': f"Payment Taken ({pay.payment_type})",
            'credit': 0,
            'debit': pay.amount,
            'type': 'debit'
        })

    # 2. Monthly Salary (Credit) - Salary on 1st
    current_date = loop_start_date.replace(day=1)
    
    while current_date <= today.replace(day=1):
        last_day = current_date + relativedelta(months=1) - timedelta(days=1)
        
        monthly_salary = staff.monthly_salary
        leaves = StaffLeave.objects.filter(staff=staff, start_date__gte=current_date, end_date__lte=last_day)
        total_leave_days = sum(leave.total_days() for leave in leaves)
        daily_rate = monthly_salary / 30 
        deduction = daily_rate * total_leave_days
        net_salary = monthly_salary - deduction

        all_transactions.append({
            'date': current_date, 
            'description': f"Salary Credited ({current_date.strftime('%B %Y')})",
            'credit': net_salary,
            'debit': 0,
            'type': 'credit'
        })

        current_date += relativedelta(months=1)

    # 3. Sort (Oldest first for calculation)
    all_transactions.sort(key=lambda x: (x['date'], 0 if x['type'] == 'credit' else 1))

    # 4. Calculate Balance
    running_balance = 0
    final_ledger = []
    
    for trans in all_transactions:
        running_balance = running_balance + trans['credit'] - trans['debit']
        trans['balance'] = running_balance
        
        include_row = True
        if start_filter and str(trans['date']) < start_filter:
            include_row = False
        if end_filter and str(trans['date']) > end_filter:
            include_row = False
            
        if include_row:
            final_ledger.append(trans)

    # Note: final_ledger.reverse() hata diya gaya hai taaki purana upar dikhe
    
    context = {
        'staff': staff,
        'ledger_data': final_ledger,
        'overall_balance': running_balance,
        'start_date': start_filter,
        'end_date': end_filter,
    }
    return render(request, 'management/staff_profile.html', context)


# ==========================================
# 6. स्टाफ लिस्ट व्यू
# ==========================================
@login_required
def staff_list_view(request):
    all_staff = Staff.objects.all().order_by('name')
    return render(request, 'management/staff_list.html', {'all_staff': all_staff})


# ==========================================
# 7. स्टाफ डिटेल व्यू
# ==========================================
@login_required
def staff_detail_view(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    return render(request, 'management/staff_detail.html', {'staff': staff})


# ==========================================
# 8. Export Report (Download CSV)
# ==========================================
@login_required
def export_monthly_expenses(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="Monthly_Expense_Report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Category', 'Description', 'Canteen', 'Payment Mode', 'Amount'])

    today = date.today()
    first_day = today.replace(day=1)
    
    expenses = Expense.objects.filter(date__gte=first_day).order_by('-date')

    for expense in expenses:
        canteen_name = expense.canteen.name if expense.canteen else "General"
        writer.writerow([
            expense.date, 
            expense.category, 
            expense.description, 
            canteen_name, 
            expense.payment_mode, 
            expense.amount
        ])

    return response


# ==========================================
# 9. Print Staff Ledger (Print View)
# ==========================================
@login_required
def print_staff_ledger(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    loop_start_date = staff.joining_date if staff.joining_date else date(date.today().year, 1, 1)
    today = date.today()
    all_transactions = []

    payments = SalaryPayment.objects.filter(staff=staff)
    for pay in payments:
        all_transactions.append({ 'date': pay.date, 'description': f"Payment ({pay.payment_type})", 'credit': 0, 'debit': pay.amount, 'type': 'debit' })

    current_date = loop_start_date.replace(day=1)
    while current_date <= today.replace(day=1):
        last_day = current_date + relativedelta(months=1) - timedelta(days=1)
        monthly_salary = staff.monthly_salary
        leaves = StaffLeave.objects.filter(staff=staff, start_date__gte=current_date, end_date__lte=last_day)
        deduction = (monthly_salary / 30) * sum(l.total_days() for l in leaves)
        
        all_transactions.append({
            'date': current_date, # Salary on 1st
            'description': f"Salary Credited ({current_date.strftime('%B %Y')})",
            'credit': monthly_salary - deduction, 'debit': 0, 'type': 'credit'
        })
        current_date += relativedelta(months=1)

    all_transactions.sort(key=lambda x: (x['date'], 0 if x['type'] == 'credit' else 1))

    running_balance = 0
    final_ledger = []
    for trans in all_transactions:
        running_balance = running_balance + trans['credit'] - trans['debit']
        trans['balance'] = running_balance
        final_ledger.append(trans)
    
    return render(request, 'management/staff_ledger_print.html', {'staff': staff, 'ledger_data': final_ledger, 'overall_balance': running_balance, 'print_date': date.today()})


# ==========================================
# 10. Add Payment/Advance
# ==========================================
@login_required
def add_staff_payment(request, staff_id):
    staff = get_object_or_404(Staff, pk=staff_id)
    
    if request.method == 'POST':
        form = SalaryPaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.staff = staff 
            payment.save()
            messages.success(request, f"Payment of ₹{payment.amount} added for {staff.name}")
            return redirect('staff_profile', staff_id=staff.id) # Yahan galti thi, ab correct he
    else:
        form = SalaryPaymentForm(initial={'date': date.today(), 'payment_type': 'Advance'})

    return render(request, 'management/add_payment.html', {'form': form, 'staff': staff})


# ==========================================
# 11. Add Daily Expense
# ==========================================
@login_required
def add_expense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Expense Added Successfully! ✅")
            return redirect('home_dashboard')
    else:
        form = ExpenseForm(initial={'date': date.today()})

    return render(request, 'management/add_expense.html', {'form': form})


# ==========================================
# 12. Add Daily Income (Galla)
# ==========================================
@login_required
def add_daily_entry(request):
    if request.method == 'POST':
        form = DailyEntryForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, "Daily Income Added Successfully! 💰")
                return redirect('home_dashboard')
            except:
                messages.error(request, "Error: Is Canteen aur Date ki entry pehle se hai!")
    else:
        form = DailyEntryForm(initial={'date': date.today()})

    return render(request, 'management/add_daily_entry.html', {'form': form})
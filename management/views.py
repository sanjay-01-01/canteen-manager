# management/views.py

from django.shortcuts import render
from django.db.models import Sum
from datetime import date, timedelta
from dateutil.relativedelta import relativedelta
from .models import Canteen, Expense, Staff, SalaryPayment, StaffLeave 
from django.db.models import Sum
from datetime import date
from dateutil.relativedelta import relativedelta

from django.db.models import Sum
from .models import Canteen, Expense, Staff 
from django.shortcuts import get_object_or_404 

from django.http import JsonResponse
from .models import Canteen

# management/views.py


def home_dashboard(request):
    # 1. Date logic
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month + relativedelta(months=1) - timedelta(days=1)

    # 2. Calculation logic
    monthly_expenses_sum = Expense.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).aggregate(total_expense=Sum('amount'))['total_expense'] or 0

    monthly_payments_sum = SalaryPayment.objects.filter(
        date__gte=first_day_of_month,
        date__lte=last_day_of_month
    ).aggregate(total_paid=Sum('amount'))['total_paid'] or 0

    total_advance_paid = SalaryPayment.objects.filter(payment_type='Advance').aggregate(total_adv=Sum('amount'))['total_adv'] or 0

    # 3. Fetching Canteens and Staff Counts
    all_canteens = Canteen.objects.all().order_by('name') 
    total_canteens_count = Canteen.objects.count()
    total_staff_count = Staff.objects.count()

    # 4. Final Unified Context
    context = {
        'current_month': today.strftime("%B %Y"),
        'total_canteens': total_canteens_count, # <-- अब यह सही से शामिल है
        'total_staff': total_staff_count,       # <-- अब यह सही से शामिल है
        'all_canteens': all_canteens,          # <-- लिस्ट भी शामिल है

        # Summary data
        'monthly_expenses_sum': monthly_expenses_sum,
        'monthly_payments_sum': monthly_payments_sum,
        'total_advance_paid': total_advance_paid, 
    }

    # 5. Only ONE return statement
    return render(request, 'management/dashboard.html', context)
# management/views.py (after canteen_report function)



def payroll_summary(request):
    # 1. इस माह की तारीखें सेट करें
    today = date.today()
    first_day_of_month = today.replace(day=1)
    last_day_of_month = first_day_of_month + relativedelta(months=1) - relativedelta(days=1)

    # 2. सभी स्टाफ मेंबर को fetch करें
    all_staff = Staff.objects.all().order_by('canteen__name', 'name')
    payroll_data = []

    for staff in all_staff:
        # A. कुल एडवांस जो वापस लेना बाकी है (यह हमेशा 'Advance' टाइप के भुगतान का योग है)
        advance_paid = SalaryPayment.objects.filter(
            staff=staff,
            payment_type='Advance'
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # B. इस माह का कुल भुगतान (Monthly, Advance, Bonus, सब कुछ)
        paid_this_month = SalaryPayment.objects.filter(
            staff=staff,
            date__gte=first_day_of_month,
            date__lte=last_day_of_month
        ).aggregate(Sum('amount'))['amount__sum'] or 0

        # C. इस माह की कुल छुट्टियां
        # हम हर छुट्टी पीरियड के दिनों को जोड़ रहे हैं
        leaves_this_month_periods = StaffLeave.objects.filter(
            staff=staff,
            start_date__gte=first_day_of_month,
            end_date__lte=last_day_of_month
        )
        total_leaves = 0
        for leave in leaves_this_month_periods:
            total_leaves += leave.total_days()

        # D. अंतिम वेतन कैलकुलेशन (एक साधारण अनुमान)
        # यहाँ हम सिर्फ़ जानकारी दिखा रहे हैं; फाइनल कैलकुलेशन यूजर को खुद करना होगा
        # Gross Salary - (Paid this month) - (Deductions if any)
        # यह Final Calculation अगले एडवांस स्टेप में होगा

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

# management/views.py (after home_dashboard function)

# You'll need these imports if you don't have them yet:


def canteen_report(request, canteen_id):
    # 1. Fetch the specific Canteen or return 404
    canteen = get_object_or_404(Canteen, pk=canteen_id)

    # 2. Calculate Total Expenses associated with this Canteen
    # Uses the Expense model's 'canteen' Foreign Key
    total_canteen_expense = Expense.objects.filter(
        canteen=canteen
    ).aggregate(total_sum=Sum('amount'))['total_sum'] or 0

    # 3. Get Staff count for this Canteen
    staff_count = Staff.objects.filter(canteen=canteen).count()

    # 4. Get detailed list of expenses for the report
    detailed_expenses = Expense.objects.filter(canteen=canteen).order_by('-date')

    context = {
        'canteen': canteen,
        'total_canteen_expense': total_canteen_expense,
        'staff_count': staff_count,
        'detailed_expenses': detailed_expenses,
    }

    return render(request, 'management/canteen_report.html', context)


# management/views.py (सबसे नीचे जोड़ें)



def get_canteen_data(request):
    # डेटाबेस से सभी कैंटीनों की ID और Billing Type लाओ
    canteens = Canteen.objects.all().values('id', 'billing_type')
    
    # इसे एक डिक्शनरी में बदलो: { '1': 'DAILY', '2': 'MONTHLY', ... }
    data = {str(c['id']): c['billing_type'] for c in canteens}
    
    return JsonResponse(data)



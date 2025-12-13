from django import forms
from .models import SalaryPayment
from .models import SalaryPayment, Expense, Canteen
from .models import DailyEntry

class SalaryPaymentForm(forms.ModelForm):
    class Meta:
        model = SalaryPayment
        fields = ['amount', 'date', 'payment_type']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_type': forms.Select(attrs={'class': 'form-select'}),
        }


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['date', 'category', 'amount', 'description', 'payment_mode', 'canteen']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter Amount'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Item Name (e.g. 5kg Tomato)'}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
            'canteen': forms.Select(attrs={'class': 'form-select'}),
        }

class DailyEntryForm(forms.ModelForm):
    class Meta:
        model = DailyEntry
        fields = ['date', 'canteen', 'cash_received', 'online_received']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'canteen': forms.Select(attrs={'class': 'form-select'}),
            'cash_received': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₹ Cash Galla'}),
            'online_received': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₹ UPI/Online'}),
        }
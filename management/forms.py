from django import forms
from .models import SalaryPayment
from .models import SalaryPayment, Expense, Canteen
from .models import DailyEntry
from .models import StaffLeave

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


# management/forms.py

class DailyEntryForm(forms.ModelForm):
    class Meta:
        model = DailyEntry
        # Sirf Date, Canteen aur Paisa rakha hai (No Nasta)
        fields = ['date', 'canteen', 'cash_received', 'online_received']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'canteen': forms.Select(attrs={'class': 'form-select'}),
            'cash_received': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₹ Cash Galla'}),
            'online_received': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '₹ UPI/Online'}),
        }

# management/forms.py (Add at bottom)

class ConsumptionForm(forms.ModelForm):
    class Meta:
        model = DailyEntry
        fields = ['date', 'canteen', 'tea_qty', 'lunch_qty', 'dinner_qty', 'nasta_qty', 'normal_token_qty', 'special_token_qty', 'guest_token_qty']
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'canteen': forms.Select(attrs={'class': 'form-select', 'id': 'canteen_select'}), # ID diya hai JS ke liye
            
            # Khana
            'tea_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'lunch_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'dinner_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'nasta_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            
            # Tokens
            'normal_token_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'special_token_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
            'guest_token_qty': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'}),
        }


# management/forms.py

  # Upar import me StaffLeave add karna na bhulein

class StaffLeaveForm(forms.ModelForm):
    class Meta:
        model = StaffLeave
        fields = ['staff', 'start_date', 'end_date', 'reason']
        
        widgets = {
            'staff': forms.Select(attrs={'class': 'form-select'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Reason for leave...'}),
        }

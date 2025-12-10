# management/admin.py

from django.contrib import admin
from .models import Canteen  # अपने Canteen मॉडल को इंपोर्ट करें
from .models import Staff
from .models import StaffLeave
from .models import Expense
from .models import SalaryPayment

# Canteen मॉडल को एडमिन पैनल में रजिस्टर करें
admin.site.register(Canteen)
admin.site.register(Staff)
class StaffLeaveAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_date', 'end_date', 'total_days', 'reason')
    list_filter = ('staff', 'start_date') # फ़िल्टर करने के विकल्प जोड़ें

# StaffLeave मॉडल को कस्टम एडमिन क्लास के साथ रजिस्टर करें
admin.site.register(StaffLeave, StaffLeaveAdmin)
admin.site.register(Expense)
admin.site.register(SalaryPayment)
# management/admin.py

from django.contrib import admin
from .models import Canteen, Staff, StaffLeave, Expense, SalaryPayment, DailyEntry 
from django.utils.html import format_html # फोटो दिखाने के लिए जरूरी

# 1. Canteen Admin
class CanteenAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'billing_type')
    search_fields = ('name', 'location')

# 2. Staff Leave Admin
class StaffLeaveAdmin(admin.ModelAdmin):
    list_display = ('staff', 'start_date', 'end_date', 'total_days', 'reason',)
    list_filter = ('staff', 'start_date')

# 3. DailyEntry Admin (सरल और साफ)
class DailyEntryAdmin(admin.ModelAdmin):
    list_display = ('canteen', 'date', 'lunch_qty', 'dinner_qty', 'nasta_qty', 'tea_qty', 'total_payment_received')
    list_filter = ('canteen', 'date')
    ordering = ('-date',)
    
    # फील्ड्स का ग्रुप (JS इन्हें कंट्रोल करेगा)
    fieldsets = [
        ('Basic Info', {'fields': ('canteen', 'date')}),
        ('Daily Supply Quantities', {'fields': ('lunch_qty', 'dinner_qty', 'nasta_qty', 'tea_qty')}),
        
        # Payment अब सबके लिए है
        ('Daily Payment Received', {'fields': ('cash_received', 'online_received')}),
        
        # Token सिर्फ Monthly के लिए (JS इसे कंट्रोल करेगा)
        ('Token Details (Monthly Only)', {'fields': ('normal_token_qty', 'special_token_qty', 'guest_token_qty')}),
    ]
    
    # JS और CSS फाइलों का लिंक (कोई फोल्डर नाम नहीं, जैसा हमने तय किया था)
    class Media:
        js = ('js/daily_entry_logic.js',) 
        css = {'all': ('css/daily_entry_hide.css',)}
    
    # Payment कैलकुलेशन
    def total_payment_received(self, obj):
        cash = obj.cash_received if obj.cash_received is not None else 0
        online = obj.online_received if obj.online_received is not None else 0
        return cash + online
    total_payment_received.short_description = 'Total Payment'

class ExpenseAdmin(admin.ModelAdmin):
    # लिस्ट में 'is_paid' की जगह 'payment_mode' दिखाएं
    list_display = ('category', 'description', 'amount', 'date', 'canteen', 'payment_mode')
    list_filter = ('date', 'category', 'payment_mode', 'canteen')
    search_fields = ('description',)

# management/admin.py



class StaffAdmin(admin.ModelAdmin):
    # लिस्ट में फोटो भी दिखाएं
    list_display = ('photo_preview', 'name', 'role', 'canteen', 'phone', 'joining_date')
    search_fields = ('name', 'phone')
    list_filter = ('canteen', 'role')

    # फोटो का छोटा प्रीव्यू बनाने का फंक्शन
    def photo_preview(self, obj):
        if obj.photo:
            return format_html('<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />', obj.photo.url)
        return "No Photo"
    
    photo_preview.short_description = "Photo"

admin.site.register(Staff, StaffAdmin)

# पुराने 'admin.site.register(Expense)' को हटाकर यह लिखें:
admin.site.register(Expense, ExpenseAdmin)

# 4. सब कुछ रजिस्टर करें
admin.site.register(Canteen, CanteenAdmin)
admin.site.register(StaffLeave, StaffLeaveAdmin)
admin.site.register(SalaryPayment)
admin.site.register(DailyEntry, DailyEntryAdmin)
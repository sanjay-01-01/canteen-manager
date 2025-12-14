# management/models.py

from django.db import models
from datetime import date

# This class will create a database table named 'management_canteen'
class Canteen(models.Model):

    BILLING_CHOICES = [
        ('DAILY', 'Daily Payment/Tracking'),
        ('MONTHLY', 'Monthly Fixed Billing'),
    ]

    # Name of the Canteen (e.g., Canteen A, Factory Mess)
    name = models.CharField(max_length=100, unique=True, verbose_name="Canteen Name")

    # Location/Address of the Canteen
    location = models.CharField(max_length=255, verbose_name="Location")

    billing_type = models.CharField(
        max_length=10, 
        choices=BILLING_CHOICES, 
        default='DAILY', 
        verbose_name="Billing Type"
    )

    # Average number of lunches sent daily
    daily_lunch_count = models.IntegerField(default=0, verbose_name="Daily Lunch Count")

    # Average number of dinners sent daily
    daily_dinner_count = models.IntegerField(default=0, verbose_name="Daily Dinner Count")

    # Function to display the name in the Admin Panel
    def __str__(self):
        return self.name

    class Meta:
        # Helps with displaying names in the Admin interface
        verbose_name = "Canteen"
        verbose_name_plural = "Canteens"


# management/models.py (Canteen class के नीचे)

class Staff(models.Model):
    ROLES = [
        ('Cook', 'Cook'),
        ('Helper', 'Helper'),
    ]

    canteen = models.ForeignKey(
        Canteen, 
        on_delete=models.SET_NULL, # अगर कैंटीन डिलीट हो जाए, तो स्टाफ को NULL कर दें
        null=True, 
        blank=True,
        verbose_name="Assigned Canteen"
    )
    name = models.CharField(max_length=100, verbose_name="Staff Name")
    role = models.CharField(max_length=10, choices=ROLES, default='Helper', verbose_name="Role")
    phone = models.CharField(max_length=15, default='0000000000', verbose_name="Phone Number")
    joining_date = models.DateField(null=True, blank=True, verbose_name="Joining Date")
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monthly Salary")
    bank_account_no = models.CharField(max_length=20, blank=True, null=True,verbose_name="Bank Account No")
    ifsc_code = models.CharField(max_length=15, blank=True, null=True,verbose_name="IFSC Code")
    photo = models.ImageField(upload_to='staff_photos/', null=True, blank=True, verbose_name="Staff Photo")
    aadhar_card = models.ImageField(upload_to='staff_aadhar/', null=True, blank=True, verbose_name="Aadhar Card Photo")
    # ----------------------
    
    def __str__(self):
        return f"{self.name} ({self.role}) - {self.canteen.name if self.canteen else 'Unassigned'}"

    class Meta:
        verbose_name = "Staff Member"
        verbose_name_plural = "Staff"



class StaffLeave(models.Model):
    staff = models.ForeignKey(
        Staff, 
        on_delete=models.CASCADE, 
        verbose_name="Staff Member"
    )

    # छुट्टी शुरू होने की तारीख
    start_date = models.DateField(verbose_name="Start Date")
    # छुट्टी समाप्त होने की तारीख
    end_date = models.DateField(verbose_name="End Date")
    reason = models.TextField(null=True, blank=True, verbose_name="Reason for Leave")
    is_paid_leave = models.BooleanField(default=False, verbose_name="Paid Leave (Don't Cut Salary)")

    def total_days(self):
        """Calculates the total number of days in the leave period (inclusive)"""
        if self.start_date and self.end_date:
            # दिनों की संख्या (समाप्ति - शुरू + 1)
            delta = self.end_date - self.start_date
            return delta.days + 1
        return 0

    total_days.short_description = 'Total Days' # एडमिन पैनल में दिखने वाला नाम

    def __str__(self):
        status = "Paid" if self.is_paid_leave else "Unpaid"
        return f"{self.staff.name} - {self.start_date} to {self.end_date}"

    class Meta:
        verbose_name = "Staff Leave (Period)"
        verbose_name_plural = "Staff Leaves (Periods)"


# management/models.py (StaffLeave class के नीचे)

# management/models.py (Expense class को इससे बदलें)

class Expense(models.Model):
    # 1. खर्च की श्रेणियां (Milk, Auto, Wood जोड़ दिया गया है)
    CATEGORY_CHOICES = [
        ('Kirana', 'Kirana/Grocery'),
        ('Gas', 'Gas Cylinder/Fuel'),
        ('Vegetables', 'Vegetables (Sabzi)'),
        ('Milk', 'Milk/Dairy'),              # New
        ('Auto', 'Auto Rickshaw/Transport'), # New
        ('Wood', 'Wood/Fuel'),               # New
        ('Other', 'Other Expenses'),
    ]

    # 2. पेमेंट का तरीका (नया सिस्टम)
    PAYMENT_MODE_CHOICES = [
        ('Pending', '🔴 Pending / Due'),
        ('Cash', '🟢 Paid - Cash'),
        ('Online', '🔵 Paid - Online'),
    ]

    canteen = models.ForeignKey(
        Canteen, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Associated Canteen"
    )

    date = models.DateField(verbose_name="Date")
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category")
    description = models.CharField(max_length=255, verbose_name="Description")
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount")
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Quantity") 

    # हमने 'is_paid' हटाकर 'payment_mode' लगा दिया है
    payment_mode = models.CharField(
        max_length=20, 
        choices=PAYMENT_MODE_CHOICES, 
        default='Cash', 
        verbose_name="Payment Status"
    )

    def __str__(self):
        return f"{self.category} - {self.amount} ({self.payment_mode})"

    class Meta:
        verbose_name = "Expense Entry"
        verbose_name_plural = "Expenses"
        ordering = ['-date']
# management/models.py (Expense class के नीचे)

class SalaryPayment(models.Model):
    PAYMENT_TYPES = [
        ('Monthly', 'Monthly Salary Payment'),
        ('Advance', 'Advance Payment'),
        ('Bonus', 'Bonus'),
    ]

    # Foreign Key: किस स्टाफ मेंबर को भुगतान किया गया
    staff = models.ForeignKey(
        Staff, 
        on_delete=models.CASCADE, 
        verbose_name="Staff Member"
    )

    date = models.DateField(verbose_name="Payment Date") # भुगतान की तारीख
    payment_type = models.CharField(max_length=10, choices=PAYMENT_TYPES, verbose_name="Payment Type") # एडवांस है या मासिक वेतन
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Paid") # दी गई राशि

    notes = models.TextField(null=True, blank=True, verbose_name="Notes/Details") # कोई भी टिप्पणी (जैसे: इस माह का भुगतान)

    def __str__(self):
        return f"{self.staff.name} - {self.payment_type} on {self.date}"

    class Meta:
        verbose_name = "Salary/Advance Payment"
        verbose_name_plural = "Salary Payments" 
        ordering = ['-date']


# management/models.py (SalaryPayment class के नीचे)

class DailyEntry(models.Model):
    # 1. Foreign Key
    canteen = models.ForeignKey(
        Canteen, 
        on_delete=models.CASCADE, 
        verbose_name="Canteen Name"
    )
    date = models.DateField(default=date.today, verbose_name="Entry Date")

    # 2. Daily Supplies (Items and Quantity)
    # Shree Aaiji Canteen: Daily variable supply. Other Canteens: Fixed supply tracking.
    lunch_qty = models.IntegerField(default=0, verbose_name="Lunch Qty")
    dinner_qty = models.IntegerField(default=0, verbose_name="Dinner Qty")
    nasta_qty = models.IntegerField(default=0, verbose_name="Nasta Qty")
    tea_qty = models.IntegerField(default=0, verbose_name="Tea Qty") # Shree Aaiji only

    normal_token_qty = models.IntegerField(default=0, verbose_name="Normal Token Qty")
    special_token_qty = models.IntegerField(default=0, verbose_name="Special Token Qty")
    guest_token_qty = models.IntegerField(default=0, verbose_name="Guest Token Qty")

    # ... (Cash और Online फील्ड्स पहले से ही यहाँ हैं, उन्हें वैसे ही रहने दें) ...
    cash_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, verbose_name="Cash Payment Received")
    online_received = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, verbose_name="Online Payment Received")

    # 3. Payment Tracking (Conditional for DAILY Billing Type)
    # If Canteen.billing_type is 'DAILY', these fields are mandatory/visible.
    cash_received = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    default=0.00, 
    null=True, # <--- यह जोड़ें
    verbose_name="Cash Payment Received"
    )
    online_received = models.DecimalField(
    max_digits=10, 
    decimal_places=2, 
    default=0.00, 
    null=True, # <--- यह जोड़ें
    verbose_name="Online Payment Received"
    )

    def __str__(self):
        return f"{self.canteen.name} - Entry on {self.date}"

    class Meta:
        verbose_name = "Daily Service/Payment Entry"
        verbose_name_plural = "Daily Entries"
        unique_together = ('canteen', 'date') # एक कैंटीन में एक दिन में सिर्फ एक एंट्री
        ordering = ['-date', 'canteen__name']

class Payroll(models.Model):
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)
    month = models.DateField() # Sirf month aur year store karenge (e.g., 1st Dec 2025)
    total_days = models.IntegerField(default=30)
    working_days = models.IntegerField(default=0)
    
    # Leaves breakdown
    paid_leaves = models.IntegerField(default=0)
    unpaid_leaves = models.IntegerField(default=0)
    
    # Money breakdown
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    deduction_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2)
    
    generated_on = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Payslip: {self.staff.name} - {self.month.strftime('%B %Y')}"



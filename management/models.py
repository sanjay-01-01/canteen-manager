# management/models.py

from django.db import models
from datetime import date

# This class will create a database table named 'management_canteen'
class Canteen(models.Model):
    # Name of the Canteen (e.g., Canteen A, Factory Mess)
    name = models.CharField(max_length=100, unique=True, verbose_name="Canteen Name")

    # Location/Address of the Canteen
    location = models.CharField(max_length=255, verbose_name="Location")

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

    joining_date = models.DateField(verbose_name="Joining Date")
    monthly_salary = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monthly Salary")

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

    def total_days(self):
        """Calculates the total number of days in the leave period (inclusive)"""
        if self.start_date and self.end_date:
            # दिनों की संख्या (समाप्ति - शुरू + 1)
            delta = self.end_date - self.start_date
            return delta.days + 1
        return 0

    total_days.short_description = 'Total Days' # एडमिन पैनल में दिखने वाला नाम

    def __str__(self):
        return f"{self.staff.name} - {self.start_date} to {self.end_date}"

    class Meta:
        verbose_name = "Staff Leave (Period)"
        verbose_name_plural = "Staff Leaves (Periods)"


# management/models.py (StaffLeave class के नीचे)

class Expense(models.Model):
    # खर्च की श्रेणियां
    CATEGORY_CHOICES = [
        ('Kirana', 'Kirana/Grocery'),
        ('Gas', 'Gas Cylinder/Fuel'),
        ('Salary', 'Salary/Wages'),
        ('Other', 'Other Expenses'),
    ]

    # Foreign Key: किस कैंटीन का खर्च है (NULL हो सकता है अगर यह जनरल खर्च है, जैसे: हेड ऑफिस का किराना)
    canteen = models.ForeignKey(
        Canteen, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Associated Canteen"
    )

    date = models.DateField(auto_now_add=True, verbose_name="Date") # खर्च की तारीख
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name="Category") # खर्च की श्रेणी
    description = models.CharField(max_length=255, verbose_name="Description") # सामान का विवरण (जैसे: 10kg Wheat Flour)
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount") # खर्च की राशि

    # जैसे: गैस के 2 सिलेंडर या 50 Kg चावल
    quantity = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Quantity") 

    # यह चेक करने के लिए कि भुगतान किया गया है या यह बकाया है
    is_paid = models.BooleanField(default=True, verbose_name="Paid Status") 

    def __str__(self):
        return f"{self.category} - {self.description} ({self.date})"

    class Meta:
        verbose_name = "Expense Entry"
        verbose_name_plural = "Expenses"
        ordering = ['-date'] # सबसे नया खर्च पहले दिखे


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
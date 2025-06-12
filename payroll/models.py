from django.db import models
from employees.models import Employee_data
from datetime import date
from django.db.models import Sum
from decimal import Decimal
from calendar import monthrange
class Payroll(models.Model):
    employee = models.ForeignKey(Employee_data, to_field='employee_id', on_delete=models.CASCADE)
    month = models.DateField()  # e.g., "2024-05-01" (use first day of month)
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    total_hours = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    performance_bonus = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False, default=0)  # Editable=False ensures it cannot be updated directly
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=[
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('paid', 'Paid')
    ], default='pending')

    class Meta:
        unique_together = ('employee', 'month')  # One payroll per employee per month

    # def calculate_total_salary(self):
    #     total_additions = sum(
    #         c.amount for c in self.payrollcomponent_set.filter(component__is_deduction=False)
    #     )
    #     total_deductions = sum(
    #         c.amount for c in self.payrollcomponent_set.filter(component__is_deduction=True)
    #     )
    #     return self.basic_salary + total_additions - total_deductions

 

    def save(self, *args, **kwargs):
        # Only auto-set total_salary if it's not set manually
        if self.total_salary is None:
            self.total_salary = self.basic_salary + self.overtime + self.bonus
       
        # Set start_date and end_date based on the month field if they aren't already set
        if self.month and (not self.start_date or not self.end_date):
            year = self.month.year
            month = self.month.month
            self.start_date = date(year, month, 1)
            last_day = monthrange(year, month)[1]
            self.end_date = date(year, month, last_day)

        super().save(*args, **kwargs)
   

   


    def __str__(self):
        return f"Payroll for {self.employee} - {self.month}"



class DailyPayroll(models.Model):
    employee = models.ForeignKey(Employee_data, to_field='employee_id', on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    daily_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    overtime = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Overtime
    overtimepay = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Overtime
    


    class Meta:
        unique_together = ('employee', 'date')

    def save(self, *args, **kwargs):
        if not self.daily_salary or self.daily_salary == Decimal("0.00"):
            self.daily_salary = self.hours_worked * self.hourly_rate
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Daily Payroll for {self.employee.name} on {self.date}"





# models.py
class PayrollSettings(models.Model):
    overtime_rate = models.DecimalField(default=100.0, max_digits=10, decimal_places=2)





















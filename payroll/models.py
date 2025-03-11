from django.db import models
from employees.models import Employee_data

class SalaryComponent(models.Model):
    name = models.CharField(max_length=50)  # e.g., "Overtime", "Tax"
    is_deduction = models.BooleanField(default=False)  # True for deductions

class Payroll(models.Model):
    # Update the ForeignKey to use the 'employee_id' field from Employee_data
    employee = models.ForeignKey(Employee_data, to_field='employee_id', on_delete=models.CASCADE)

    month = models.DateField()  # e.g., "2024-05-01"
    basic_salary = models.DecimalField(max_digits=10, decimal_places=2)
    components = models.ManyToManyField(SalaryComponent, through='PayrollComponent')
    total_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate total salary (basic + additions - deductions)
        self.total_salary = self.basic_salary + sum(
            c.amount for c in self.payrollcomponent_set.filter(component__is_deduction=False)
        ) - sum(
            c.amount for c in self.payrollcomponent_set.filter(component__is_deduction=True)
        )
        super().save(*args, **kwargs)

class PayrollComponent(models.Model):
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE)
    component = models.ForeignKey(SalaryComponent, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)


 # class DailyPayroll(models.Model):
    #     employee = models.ForeignKey(Employee_data, to_field='employee_id', on_delete=models.CASCADE)
    #     date = models.DateField(default=date.today)  # Store payroll per day
    #     hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    #     hourly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    #     daily_salary = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    #     def save(self, *args, **kwargs):
    #         self.daily_salary = self.hours_worked * self.hourly_rate
    #         super().save(*args, **kwargs)
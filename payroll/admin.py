from django.contrib import admin

# Register your models here.
from .models import DailyPayroll, Payroll

# admin.site.register(SalaryComponent)
admin.site.register(DailyPayroll)

admin.site.register(Payroll)
# admin.site.register(PayrollComponent)
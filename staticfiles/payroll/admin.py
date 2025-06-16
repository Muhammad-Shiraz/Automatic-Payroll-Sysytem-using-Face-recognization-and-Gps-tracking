from django.contrib import admin

# Register your models here.
from .models import DailyPayroll, Payroll

admin.site.register(DailyPayroll)

admin.site.register(Payroll)
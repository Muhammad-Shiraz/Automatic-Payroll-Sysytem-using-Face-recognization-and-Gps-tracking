from django.contrib import admin

# Register your models here.
from .models import SalaryComponent

admin.site.register(SalaryComponent)
# admin.site.register(Payroll)
# admin.site.register(PayrollComponent)
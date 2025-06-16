from django.contrib import admin
from .models import PerformanceBonusRule,PerformanceKPI,EmployeePerformance

admin.site.register(PerformanceBonusRule)
admin.site.register(PerformanceKPI)
admin.site.register(EmployeePerformance)

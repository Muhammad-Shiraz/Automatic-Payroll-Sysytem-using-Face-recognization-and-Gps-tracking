from django.contrib import admin
from .models import Department, Designation, Employee_data

admin.site.register(Department)
admin.site.register(Designation)
admin.site.register(Employee_data)
from django.contrib import admin

# Register your models here.
from complaints.models import Complaint,EmployeeFeedback

admin.site.register(Complaint)
admin.site.register(EmployeeFeedback)